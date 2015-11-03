#************************************************************************************************************
# Program Name: Big2small_GUI
# Program Info: when dealing with big data files, ArcMap normally won't be able to handle the process easily.
# In such cases, we will need to clip the big data file into pieces with specific index ids and make data process accordingly.
# The script below will help user create small grid files that contain partial data out of the entire dataset
# Program created date:2015-10-19
# Created by: AAFC-JiaQi Guo(Max)
# Modified date:2015-10-28
# Modified part:Add the userinput # of fishnet grid and userinput name, line 435 ~ line 460
# Modified part:Add export_ASCII options line:435 ~ 448, in exact value to point function
# Modified part:Add timer by printing current start time and current end time
# Modiferd part:Add select method, only export the fishnet with values line 333 ~ line 364
# Modified part:Add the checking if files are exist, if so output, line 461 ~ line 488
# Modified part:Convert all the dbf files to csv files, line 505 ~ line 525 import modual csv. 
#******************************************************************************************************************
# Potential utilization: elimate the fishnet grid with no data
# Adding the progress bar/timer? Line 195
#******************************************************************************************************************
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
        self.quit = Button(frame, text="QUIT", fg="red", font=("Arial", 12,"bold"),command=frame.quit)
        self.centre = Button(frame, text="Centroid from ResampleGrid",font=("Arial", 12,"bold"), command=self.Rsample)   
        self.clip = Button(frame, text="Get FishnetGrid with PtData", font=("Arial", 12,"bold"),command=self.Fclip)
        self.value2p = Button(frame, text="Extract value to Point",font=("Arial", 12,"bold"), command=self.Val2Pt)
        self.tip = Button(frame, text="**Program Info**", fg="blue",font=("Arial", 12,"bold"), command=self.tips)

        t1 = Label(frame, text = "Select the file which needs to resample find the centroid",fg ="dark green", font= ("Helvetica 10 bold italic"))
        t2 = Label(frame, text = "Clip the AOI,add the fishnet, X Y coordiate value and outputs all the grids.",fg ="dark green",font= ("Helvetica 10 bold italic"))
        t3 = Label(frame, text = "Extract multi-value to points from a index range",fg ="dark green",font= ("Helvetica 10 bold italic"))

        t1.grid(row=2, column=2, padx=2, pady=5, sticky="W")
        t2.grid(row=3, column=2, padx=2, pady=5, sticky="W")
        t3.grid(row=4, column=2, padx=2, pady=5, sticky="W")


        self.centre.grid(row=2, column=1, padx=5, pady=5, sticky="W")
        self.clip.grid(row=3, column=1, padx=5, pady=5, sticky="W")
        self.value2p.grid(row=4, column=1, padx=5, pady=5, sticky="W")
        self.quit.grid(row=8, column=3, sticky="W")
        self.tip.grid(row=8, column=1, sticky="W")

## writting help file inside of the GUI

    def tips(self):
        
        newW = Toplevel(root)
        newW.title("Program Info")
        newW.resizable(0,0)
        w1 = Label(newW, text = "Content",
                    font=("Arial", 11, "bold"))
        w1.pack()
        
        w2 = Message(newW,
                    text = " Nowadays, the spatial data has becoming bigger and bigger, when dealing with big data files,"
                     "ArcMap norammly won't be able to handle the process easily "
                     "In such cases, we will need to clip the big data file into pieces with specific index id and make data process accordingly.",
                    borderwidth = 7,
                    font=("Arial", 12),
                    anchor = "w")
        w2.pack()
        
        w3 = Label(newW,text = "Approach",
                    font=("Arial", 11, "bold"))
        w3.pack()

        w4 = Message(newW,
                    text = "The program will create a fishnet grids using the user input number of rows and columns based on the content of the AOI,"
                     "and make spatial process grid by grid.",
                    borderwidth = 7,
                    font=("Arial", 12),
                    anchor = "w")
        w4.pack()

        w5 = Label (newW, text = "                  2015-10-19. AAFC",fg="red",font=("Arial", 11, "bold"))

        w5.pack()


    def Rsample(self):


# Setting up the Sub-GUI for "Resample"

        newW = Toplevel(root)
        newW.title("Resample to centroid")
        newW.resizable(0,0)

        file_label1 = Label(newW, text="Grid file need to resample:",font=("Arial", 11))
        IFile = Entry(newW, width=50)
        file_browse_button1 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,IFile, "Select a file", "openOfile"))

        file_label2 = Label(newW, text="Choose the working folder:",font=("Arial", 11))
        Ofile = Entry(newW, width=50)
        file_browse_button2 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,Ofile, "Select a working folder", "workingfolder"))

        file_label3 = Label(newW, text="Output cell size X,Y:",font=("Arial", 11))
        Snumx = Entry(newW, width=10)
        Snumy = Entry(newW, width=10)

        file_label4 = Label(newW, text="Resample type:",font=("Arial", 11))

        Stype = StringVar(newW)
        Stype.set("NEAREST") # initial value
        
        option = OptionMenu(newW, Stype, "NEAREST", "BILINEAR", "CUBIC", "MAJORITY")

        
        run_button = Button(newW, text="RUN",fg="red",font=("Arial", 11, "bold"),command=lambda: run(IFile.get(),
                                                                                                     Ofile.get(),
                                                                                                     Snumx.get(),
                                                                                                     Snumy.get(),
                                                                                                     Stype.get()))



        file_label1.grid(row=2, column=1, padx=5, pady=5, sticky="E")
        IFile.grid(row=2, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button1.grid(row=2, column=5, padx=5, pady=5)
        
        file_label2.grid(row=3, column=1, padx=5, pady=5, sticky="E")
        Ofile.grid(row=3, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button2.grid(row=3, column=5, padx=5, pady=5)
        
        file_label3.grid(row=4, column=1, padx=5, pady=5, sticky="E")
        Snumx.grid(row=4, column=2, columnspan=3, padx=5, pady=5,sticky="W")
        Snumy.grid(row=4, column=3, columnspan=3, padx=5, pady=5,sticky="W")
        
        file_label4.grid(row=5, column=1, padx=5, pady=5, sticky="E")

        option.grid(row=5, column=2, columnspan=3, padx=5, pady=5,sticky="W")

        run_button.grid(row=5,column=5, padx=5, pady=5, sticky="E")



        def browse(newW,textbox,dialogtitle, type, mustexist=1, filetypes=[("All","*")]):
    
            if(type=="openOfile"):
                case = tkFileDialog.askopenfilename(parent=newW,title = "Select the file need to resample:",filetypes=filetypes)
            elif(type=="workingfolder"):
                case = tkFileDialog.askdirectory(parent=newW,title = "Specify the output file folder:",mustexist=mustexist)
                
            else:
                raise ValueError(type + " is not a valid browse dialog type.")
                return

            if(len(case)>0):
                dir = os.path.dirname(case)
                textbox.delete(0, END)
                textbox.insert(0, case)


        def run (IFile, Ofile, Snumx, Snumy, Stype):
            from arcpy import env
            env.overwriteOutput = "True"
            print "--------------------------------------------------------------------"
            print "Program GetCentroid Starts: ",time.asctime( time.localtime(time.time()) )
            print "--------------------------------------------------------------------"
            try:
                import arcpy
                from arcpy import env
                arcpy.env.workspace = Ofile
                cell = Snumx +" "+Snumy
                # Resample TIFF image 
                arcpy.Resample_management(IFile, "resamplenew.tif", cell, Stype)

                inRaster = "resamplenew.tif"
                outPoint = Ofile + "/outpoint.shp"
                field = "VALUE"
                arcpy.RasterToPoint_conversion(inRaster, outPoint, field)

                print "Input corret, output file has been generated..!"
                print "--------------------------------------------------------------------"
                print "Program GetCentroid Ends: ",time.asctime( time.localtime(time.time()) )
                print "--------------------------------------------------------------------"

            except:
                print "Resample example failed."
                print arcpy.GetMessages()

				
				
				
                
    def Fclip(self):

        newW = Toplevel(root)
        newW.title("Create Fishnet of the AOI with index")
        newW.resizable(0,0)

##        progressbar = ttk.Progressbar(orient=HORIZONTAL, length=200, mode='determinate')
##        progressbar.pack(side="bottom")
##        progressbar.start()

        file_label1 = Label(newW, text="The point file need to be cliped:",font=("Arial", 11))
        IFile = Entry(newW, width=50)
        file_browse_button1 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,IFile, "Select a file", "openOfile"))
        
        file_label2 = Label(newW, text="The feature to clip the input features(provincial polygon):",font=("Arial", 11))
        CFile = Entry(newW, width=50)
        file_browse_button2 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,CFile, "Select a file", "openCfile"))

        file_label3 = Label(newW, text="Choose the working directory:",font=("Arial", 11))
        OFile = Entry(newW, width=50)
        file_browse_button3 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,OFile, "Select a folder", "workingfolder"))

        file_label4 = Label(newW, text="Reference file of the fishnet(normally provincial polygon):",font=("Arial", 11))
        RFile = Entry(newW, width=50)
        file_browse_button4 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,RFile, "Select a file", "openRfile"))

        file_label5 = Label(newW, text="Input the fishnet rows and columns:",font=("Arial", 11))
        Rnum = Entry(newW, width=10)
        Cnum = Entry(newW, width=10)
        
        run_button = Button(newW, text="RUN",fg="red",font=("Arial", 11, "bold"),command=lambda: run(IFile.get(),
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



        def browse(newW,textbox,dialogtitle, type, mustexist=1, filetypes=[("All","*")]):

                if(type=="openOfile"):
                        case = tkFileDialog.askopenfilename(parent=newW,title = "Select the file need to be cliped:",filetypes=filetypes)
                elif(type=="openCfile"):
                        case = tkFileDialog.askopenfilename(parent=newW,title = "Select the file use to clip:",filetypes=filetypes)
                elif(type=="openRfile"):
                        case = tkFileDialog.askopenfilename(parent=newW,title = "Select the fishnet extent reference file:",filetypes=filetypes)     
                        
                elif(type=="workingfolder"):
                        case = tkFileDialog.askdirectory(parent=newW,title = "Specify the output file folder:",mustexist=mustexist)
                        
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
                out_feature_class = OFile + "/AOI.shp"
                xy_tolerance =""
                arcpy.Clip_analysis(in_features, clip_feature, out_feature_class, xy_tolerance)

                ## running add XY coordinate tool 
                in_feature = "AOI.shp"
                arcpy.AddXY_management(in_feature)

                ## Add fishnet, the extent will be based on AOI

                lstR = arcpy.Describe(RFile) 

                outFeatureClass = OFile + "/AOI_fishnet10by10.shp"
                
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

                lyrFishnet = arcpy.MakeFeatureLayer_management("AOI_fishnet10by10.shp", "lyr_poly")
                lyrAOI = arcpy.MakeFeatureLayer_management("AOI.shp", "lyr_pts")

                rowsFishnet = arcpy.SearchCursor(lyrFishnet)

                for row1 in rowsFishnet:

                    
                    lyrSelection = arcpy.SelectLayerByAttribute_management(lyrFishnet,"NEW_SELECTION", "\"FID\" = " + str(row1.FID))
                    
                    lyrResult = arcpy.SelectLayerByLocation_management(lyrAOI, "COMPLETELY_WITHIN", lyrSelection, "", "NEW_SELECTION")


                    desc = arcpy.Describe(lyrResult)
                    
                    if desc.fidSet != '':
                        arcpy.CopyFeatures_management(lyrResult, "selected_features" + str(row1.FID))
                        print "Value of grid " + str(row1.FID) + " has been successfully generated."
                    else:
                        print str(row1.FID) + " This field has no value."
                del lyrFishnet
                del lyrAOI
                del row1
                del rowsFishnet
                print "All the grid points have been successfully generated!"
                print "--------------------------------------------------------------------"
                print "Program ClipIntoFishnet Ends: ",time.asctime( time.localtime(time.time()) )
                print "--------------------------------------------------------------------"

				
                
    def Val2Pt(self):


        # Setting up the Sub-GUI for "Val2Pt"

        newW = Toplevel(root)
        newW.title("Value to points")
        newW.resizable(0,0)

        file_label1 = Label(newW, text="Value need to extract into points:",font=("Arial", 11))
        IFile = Entry(newW, width=50)
        file_browse_button1 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,IFile, "Select a file", "openOfile"))

        file_label2 = Label(newW, text="Choose the working folder:",font=("Arial", 11))
        Ofile = Entry(newW, width=50)
        file_browse_button2 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,Ofile, "Select a folder", "workingfolder"))

        file_label3 = Label(newW, text="#fishnet grid(based on #fishnet created early):",font=("Arial", 11))
        Fnum = Entry(newW, width=10)
        
        file_label4 = Label(newW, text="new field name(less than 10 caracter) :",font=("Arial", 11))
        Nfield = Entry(newW, width=10)

        file_label5 = Label(newW,text="Output current field in ASCII format?",font=("Arial", 11))
        Aout = StringVar(newW)
        Aout.set("No") # initial value
        option1 = OptionMenu(newW, Aout, "Yes", "No")

        t4 = Label(newW, text = "new input field value to text file",fg ="dark green", font= ("Helvetica 10 bold italic"))
        t5 = Label(newW, text = "dbf file for every grid to CSV file",fg ="dark green", font= ("Helvetica 10 bold italic"))

        t4.grid(row=5, column=4, padx=2, pady=5, sticky="E")
        t5.grid(row=6, column=4, padx=2, pady=5, sticky="E")
        
        
        file_label6 = Label(newW,text="Output all the data in ASCII format?",font=("Arial", 11))
        Csvout = StringVar(newW)
        Csvout.set("No") # initial value
        
        option2 = OptionMenu(newW, Csvout, "Yes", "No")
        

        run_button = Button(newW, text="RUN",fg="red",font=("Arial", 11, "bold"),command=lambda: run(IFile.get(),
                                                                                                     Ofile.get(),
                                                                                                     Fnum.get(),
                                                                                                     Nfield.get(),
                                                                                                     Aout.get(),
												     Csvout.get()))



        file_label1.grid(row=2, column=1, padx=5, pady=5, sticky="E")
        IFile.grid(row=2, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button1.grid(row=2, column=5, padx=5, pady=5)
        
        file_label2.grid(row=3, column=1, padx=5, pady=5, sticky="E")
        Ofile.grid(row=3, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button2.grid(row=3, column=5, padx=5, pady=5)

        file_label3.grid(row=4, column=1, padx=5, pady=5, sticky="E")
        Fnum.grid(row=4, column=2, columnspan=3, padx=5, pady=5,sticky="W")

        file_label4.grid(row=4, column=4, padx=5, pady=5, sticky="E")
        Nfield.grid(row=4, column=5, columnspan=3, padx=5, pady=5,sticky="W")
        
        file_label5.grid(row=5, column=1, padx=5, pady=5, sticky="E")
        option1.grid(row=5, column=2, columnspan=3, padx=5, pady=5,sticky="W")
		
        file_label6.grid(row=6, column=1, padx=5, pady=5, sticky="E")
        option2.grid(row=6, column=2, columnspan=3, padx=5, pady=5,sticky="W")		
        
        run_button.grid(row=6,column=5, padx=5, pady=5, sticky="E")



        def browse(newW,textbox,dialogtitle, type, mustexist=1, filetypes=[("All","*")]):

                if(type=="openOfile"):
                        case = tkFileDialog.askopenfilename(parent=newW,title = "Select the file need to exact the value from:",filetypes=filetypes)                        
                elif(type=="workingfolder"):
                        case = tkFileDialog.askdirectory(parent=newW,title = "Specify the output file:",mustexist=mustexist)
                        
                else:
                        raise ValueError(type + " is not a valid browse dialog type.")
                        return

                if(len(case)>0):
                        dir = os.path.dirname(case)
                        textbox.delete(0, END)
                        textbox.insert(0, case)


        def run (IFile, Ofile,Fnum,Nfield,Aout,Csvout):

            import arcpy
            import os
            import os.path
            from arcpy import env
            env.overwriteOutput = "True"

            # Set environment settings
            env.workspace = Ofile


            # Set local variables
            print "--------------------------------------------------------------------"
            print "Program ExtractValue2Point Starts: ",time.asctime( time.localtime(time.time()) )
            print "--------------------------------------------------------------------"
            for x in xrange(0,int(Fnum)):
                if (Aout == "Yes"):

                    if os.path.isfile(Ofile + "/" + "selected_features" + str(x) +".shp" ):
                        print "output value of Grid " , x
                        print ""
                        inFeatures = "selected_features" + str(x) +".shp"
                        export_ASCII = "ASCII " + str(x) +".txt"
                        inRasterList = [[IFile, str(Nfield)]]
                        
                        # Check out the ArcGIS Spatial Analyst extension license
                        arcpy.CheckOutExtension("Spatial")

                        # Execute ExtractValuesToPoints
                        ExtractMultiValuesToPoints(inFeatures, inRasterList, "BILINEAR")
                        arcpy.ExportXYv_stats(inFeatures, str(Nfield),"SPACE", export_ASCII,"ADD_FIELD_NAMES")
                 
                else:
                    if os.path.isfile(Ofile + "/" + "selected_features" + str(x) +".shp" ):
                        print "output value of Grid " , x
                        print ""
                        inFeatures = "selected_features" + str(x) +".shp"
                        inRasterList = [[IFile, str(Nfield)]]

                        # Check out the ArcGIS Spatial Analyst extension license
                        arcpy.CheckOutExtension("Spatial")

                        # Execute ExtractValuesToPoints
                        ExtractMultiValuesToPoints(inFeatures, inRasterList, "BILINEAR")

            if (Csvout == "Yes"):
                for x in xrange(0,int(Fnum)):
                    if os.path.isfile(Ofile + "/" + "selected_features" + str(x) +".shp" ):
                        filename = Ofile + "/selected_features" + str(x) + ".dbf"
                        if filename.endswith('.dbf'):
                            print "Converting %s to csv" % filename
                            csv_fn = filename[:-4]+ ".csv"
                            with open(csv_fn,'wb') as csvfile:
                                in_db = dbf.Dbf(filename)
                                out_csv = csv.writer(csvfile)
                                names = []
                                for field in in_db.header.fields:
                                                            names.append(field.name)
                                out_csv.writerow(names)
                                for rec in in_db:
                                    out_csv.writerow(rec.fieldData)
                                in_db.close()
                                print "Done..."
                        else:
                             print "Filename does not end with .dbf"
            else:
                print "-------------------------------------------"
                print "Not generating all the csv files"
                     
                

            print ""
            print "the value has been added to all the grid file"
            print "the ASCII files have been generated"
            print "--------------------------------------------------------------------"
            print "Program ExtractValue2Point Ends: ",time.asctime( time.localtime(time.time()) )
            print "--------------------------------------------------------------------"
            





root = Tk()

root.title("Simple GUI")
root.resizable(0,0)
app = App(root)
root.mainloop()
root.destroy() 
