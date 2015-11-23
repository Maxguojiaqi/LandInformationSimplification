# This is a standlone code for soilland cliping using fishnet
# This creats raster files to help reduce the file size


from Tkinter import *
import ttk
import csv
from dbfpy import dbf
import tkSimpleDialog
import tkFileDialog
import tkMessageBox
import os
import arcpy
import time
import sys
from arcpy.sa import *

class App:


    def __init__(self, master):

            frame = Frame(master)
            frame.pack()

            file_label1 = Label(frame, text="The DEM file need to be cliped:",font=("Arial", 11))
            IFile = Entry(frame, width=50)
            file_browse_button1 = Button(frame,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(frame,IFile, "Select a file", "openOfile"))
            
            file_label2 = Label(frame, text="The feature to clip the DEM file(provincial polygon):",font=("Arial", 11))
            CFile = Entry(frame, width=50)
            file_browse_button2 = Button(frame,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(frame,CFile, "Select a file", "openCfile"))

            file_label3 = Label(frame, text="Choose the working directory:",font=("Arial", 11))
            OFile = Entry(frame, width=50)
            file_browse_button3 = Button(frame,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(frame,OFile, "Select a folder", "workingfolder"))

            file_label4 = Label(frame, text="Reference file of the fishnet(normally provincial polygon):",font=("Arial", 11))
            RFile = Entry(frame, width=50)
            file_browse_button4 = Button(frame,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(frame,RFile, "Select a file", "openRfile"))

            file_label5 = Label(frame, text="Input the fishnet rows and columns:",font=("Arial", 11))
            Rnum = Entry(frame, width=10)
            Cnum = Entry(frame, width=10)
            
            run_button = Button(frame, text="RUN",fg="red",font=("Arial", 11, "bold"),command=lambda: run(IFile.get(),
                                                                                                         CFile.get(),
                                                                                                         OFile.get(),
                                                                                                         RFile.get(),
                                                                                                         Rnum.get(),
                                                                                                         Cnum.get()))

            file_label1.grid(row=2, column=1, padx=5, pady=5, sticky="E")
            IFile.grid(row=2, column=2, columnspan=3, padx=5, pady=5)
            file_browse_button1.grid(row=2, column=5, padx=5, pady=5)
                            
            file_label2.grid(row=3, column=1, padx=5, pady=5, sticky="E")
            CFile.grid(row=3, column=2, columnspan=3, padx=5, pady=5)
            file_browse_button2.grid(row=3, column=5, padx=5, pady=5)
            
            file_label3.grid(row=4, column=1, padx=5, pady=5, sticky="E")
            OFile.grid(row=4, column=2, columnspan=3, padx=5, pady=5)
            file_browse_button3.grid(row=4, column=5, padx=5, pady=5)

            file_label4.grid(row=5, column=1, padx=5, pady=5, sticky="E")
            RFile.grid(row=5, column=2, columnspan=3, padx=5, pady=5)
            file_browse_button4.grid(row=5, column=5, padx=5, pady=5)

            file_label5.grid(row=6, column=1, padx=5, pady=5, sticky="E")
            Rnum.grid(row=6, column=2, columnspan=3, padx=5, pady=5,sticky="W")
            Cnum.grid(row=6, column=3, columnspan=3, padx=5, pady=5,sticky="W")
            
            run_button.grid(row=6,column=5, padx=5, pady=5, sticky="E")



            def browse(frame,textbox,dialogtitle, type, mustexist=1, filetypes=[("All","*")]):

                    if(type=="openOfile"):
                            case = tkFileDialog.askopenfilename(parent=frame,title = "Select the file need to be cliped:",filetypes=filetypes)
                    elif(type=="openCfile"):
                            case = tkFileDialog.askopenfilename(parent=frame,title = "Select the file use to clip:",filetypes=filetypes)
                    elif(type=="openRfile"):
                            case = tkFileDialog.askopenfilename(parent=frame,title = "Select the fishnet extent reference file:",filetypes=filetypes)     
                            
                    elif(type=="workingfolder"):
                            case = tkFileDialog.askdirectory(parent=frame,title = "Specify the output file folder:",mustexist=mustexist)
                            
                    else:
                            raise ValueError(type + " is not a valid browse dialog type.")
                            return

                    if(len(case)>0):
                            dir = os.path.dirname(case)
                            textbox.delete(0, END)
                            textbox.insert(0, case)


            def run (IFile, CFile, OFile, RFile, Rnum, Cnum):
                    import arcpy
                    from arcpy import env
                    env.overwriteOutput = "True"
                    print "--------------------------------------------------------------------"
                    print "Program ClipIntoFishnet Starts: ",time.asctime( time.localtime(time.time()) )
                    print "--------------------------------------------------------------------"
                    ## Clip the file into the are of interest
                    arcpy.env.workspace = OFile
                    in_features = IFile
                    clip_feature = CFile
                    out_feature_class = OFile + "/AOI.tif"
                    arcpy.Clip_management(in_features, "#",out_feature_class,clip_feature,"0","ClippingGeometry")

                    ## Add fishnet, the extent will be based on AOI

                    lstR = arcpy.Describe(RFile) 

                    outFeatureClass = OFile + "/AOI_fishnet.shp"
                    
                    originCoordinate = str(lstR.extent.XMin) + " " + str(lstR.extent.YMin)
                    yAxisCoordinate = str(lstR.extent.XMin) + " " + str(lstR.extent.YMax)
                    cellSizeWidth = '0'
                    cellSizeHeight = '0'
                    numRows =  str(Rnum)
                    numColumns = str(Cnum)
                    oppositeCoorner = str(lstR.extent.XMax) + " " + str(lstR.extent.YMax)
                    labels = 'NO_LABELS'
                    templateExtent = RFile
                    geometryType = 'POLYGON'

                    arcpy.CreateFishnet_management(outFeatureClass,
                                                   originCoordinate,
                                                   yAxisCoordinate,
                                                   cellSizeWidth,
                                                   cellSizeHeight,
                                                   numRows,
                                                   numColumns,
                                                   oppositeCoorner,
                                                   labels,
                                                   templateExtent,
                                                   geometryType)






                    ## Outputting all the AOI points file according to the fishnet grids.
                    env.workspace = OFile
                    env.overwriteOutput = "True"

                    lyrFishnet = arcpy.MakeFeatureLayer_management("AOI_fishnet.shp", "lyr_poly")

                    rowsFishnet = arcpy.SearchCursor(lyrFishnet)

                    for row1 in rowsFishnet:

                        
                        lyrSelection = arcpy.SelectLayerByAttribute_management(lyrFishnet,"NEW_SELECTION", "\"FID\" = " + str(row1.FID))
                        
                        arcpy.CopyFeatures_management(lyrSelection, "part" + str(row1.FID))
                        print "Value of grid " + str(row1.FID) + " has been successfully generated."


                        arcpy.Buffer_analysis( "part" + str(row1.FID) + ".shp", OFile+ "/part" + str(row1.FID) + str(row1.FID)+".shp","10000 Meters", "FULL", "ROUND", "LIST", "FID")            


                        in_features_p= OFile + "/AOI.tif"
                        clip_feature_p = "part" + str(row1.FID) + str(row1.FID) + ".shp"
                        out_feature_class_p = "clippart" + str(row1.FID) + ".tif"
                        arcpy.Clip_management(in_features_p, "#",out_feature_class_p,clip_feature_p,"0","ClippingGeometry")

                        print "Created .tif file contains the grid size information:" + "clippart" + str(row1.FID) + ".tif"
                        print "-----------------------------------------------------------------------"


                        


                    print "All the grid points have been successfully generated!"
                    print "--------------------------------------------------------------------"
                    print "Program ClipIntoFishnet Ends: ",time.asctime( time.localtime(time.time()) )
                    print "--------------------------------------------------------------------"



root = Tk()

root.title("Simple GUI")
root.resizable(0,0)
app = App(root)
root.mainloop()
root.destroy()
