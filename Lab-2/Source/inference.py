from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import glob
import logging
import math
import os
import tensorflow as tf
import re
from difflib import SequenceMatcher

from medium_show_and_tell_caption_generator.caption_generator import CaptionGenerator
from medium_show_and_tell_caption_generator.model import ShowAndTellModel
from medium_show_and_tell_caption_generator.vocabulary import Vocabulary

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string("model_path", "C:\\Users\\Siri\\Downloads\\medium-show-and-tell-caption-generator-master\\medium-show-and-tell-caption-generator-master\\model\\show-and-tell.pb", "Model graph def path")
tf.flags.DEFINE_string("vocab_file", "C:\\Users\\Siri\\Downloads\\medium-show-and-tell-caption-generator-master\\medium-show-and-tell-caption-generator-master\\etc\\word_counts.txt", "Text file containing the vocabulary.")

image_list = ""
for filename in glob.glob("C:\\Users\\Siri\\Downloads\\medium-show-and-tell-caption-generator-master\\medium-show-and-tell-caption-generator-master\\imgs\\football\\*.jpg"):
    image_list += filename + ","

tf.flags.DEFINE_string("input_files", image_list,
                       "File pattern or comma-separated list of file patterns "
                       "of image files.")

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def main(_):
    model = ShowAndTellModel(FLAGS.model_path)
    vocab = Vocabulary(FLAGS.vocab_file)
    filenames = _load_filenames()

    generator = CaptionGenerator(model, vocab)

    for filename in filenames:
        with tf.gfile.GFile(filename, "rb") as f:
            image = f.read()
        captions = generator.beam_search(image)
        print("Captions for image %s:" % os.path.basename(filename))
        with open('output.txt', 'a') as f:
            f.write("Captions for image %s:" % os.path.basename(filename))
            for i, caption in enumerate(captions):
                # Ignore begin and end tokens <S> and </S>.
                sentence = [vocab.id_to_token(w) for w in caption.sentence[1:-1]]

                # For calculating accuracy
                with open('caption.txt', 'r', encoding="utf8") as file:
                    pattern = os.path.basename(filename) + '#' + str(i)
                    for item in file:
                        match = re.search(pattern, item)
                        if(match):
                            actual = item.split('\t')[1]
                            accuracy = similar(actual, sentence)

                sentence = " ".join(sentence)
                print("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)) + " - Accuracy: " + str(accuracy))
                f.write("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)) +"- Accuracy: "+ str(accuracy) + "\n")


def _load_filenames():
    filenames = []

    for file_pattern in FLAGS.input_files.split(","):
        filenames.extend(tf.gfile.Glob(file_pattern))

    logger.info("Running caption generation on %d files matching %s",
                len(filenames), FLAGS.input_files)
    return filenames


if __name__ == "__main__":
    tf.app.run()
