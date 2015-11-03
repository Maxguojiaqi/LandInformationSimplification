# LandInformationsimplification

  Program Info: when dealing with big data files, ArcMap normally won't be able to handle the process easily. In such cases, we will need to clip the big data file into pieces with specific index ids and make data process accordingly.
  
  This program will create a fishnet to cut the entire data which needs to process, use each grid of fish net to cut the Area of Interest, if there is data inside of the gird, export the data and make analysis. 
  This program will also generate ASCII data files for all the non-empty fishnet grid, eventually this program is run from a Apache Hadoop system. 
  
  
