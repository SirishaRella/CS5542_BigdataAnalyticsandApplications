

import org.apache.spark.{SparkContext, SparkConf}

object SparkWordCount {

  def main(args: Array[String]) {

    System.setProperty("hadoop.home.dir","C:\\Users\\Siri\\winutils");
    val sparkConf = new SparkConf().setAppName("SparkWordCount").setMaster("local[*]")
    val sc=new SparkContext(sparkConf)
    val input=sc.textFile("input")
    val wc=input.flatMap(line=>{line.split(" ")}).cache()
    val output=wc.groupBy(word=>word.charAt(0))
    output.saveAsTextFile("output")
    output.collect.foreach(println)
  }
}
