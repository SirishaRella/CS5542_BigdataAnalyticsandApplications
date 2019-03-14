import java.io.PrintStream

import org.apache.spark.mllib.clustering.KMeans
import org.apache.spark.mllib.feature.HashingTF
import org.apache.spark.{SparkConf, SparkContext}

object kM_Clustering {
  def main(args: Array[String]): Unit = {
    System.setProperty("hadoop.home.dir", "C:\\Users\\Siri\\Downloads\\winutils")
    val sparkConf = new SparkConf().setAppName("SparkWordCount").setMaster("local[*]")
    val sc = new SparkContext(sparkConf)

    val features=sc.textFile("data\\Flickr8k.token.txt")
      .map(f=>{
        val str=f.replaceAll(",","")
        val ff=f.split(" ")
        val out1=new PrintStream("data\\results1.csv")
        ff.drop(1).toSeq
      })
      val hashingTF=new HashingTF()

    val tf=hashingTF.transform(features)
    print(tf)
    val kMeansModel=KMeans.train(tf,10,1000)

    val WSSSE = kMeansModel.computeCost(tf)
    println("Within Set Sum of Squared Errors = " + WSSSE)

    val clusters=kMeansModel.predict(tf)
    val out=new PrintStream("data\\results.csv")
    features.zip(clusters).collect().foreach(f=>{
       out.println(f._2+","+f._1.mkString(" "))
      })
  }

}
