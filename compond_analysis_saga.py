import arcpy
import subprocess
import os
import sys
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *
arcpy.env.overwriteOutput = True

def runCommand_logged(cmd, logstd, logerr):
    p = subprocess.call(cmd, stdout=logstd, stderr=logerr)

WORKDIR = "D:/ab_tst"
STDLOG = WORKDIR + os.sep + "import.log"
ERRLOG = WORKDIR + os.sep + "import.error.log"

logstd = open(STDLOG, "a")
logerr = open(ERRLOG, "a")




dem_in = "D:/ab_tst/"
out_path = "D:/ab_tst/out/"

print dem_in
print out_path

def saga_compound(dem_in ,out_path):

    in_ELEVATION  = dem_in + "clippart0.tif"
    out_SHADE = out_path + "out_SHADE.tif"
    out_SLOPE = out_path + "out_SLOPE.tif"
    out_HCURV = out_path + "out_HCURV.tif"
    out_VCURV = out_path + "out_VCURV.tif"
    out_CONVERGENCE = out_path + "out_CONVERGENCE.tif"
    out_SINKS = out_path + "out_SINKS.tif"
    out_CAREA = out_path + "out_CAREA.tif"
    out_WETNESS = out_path + "out_WETNESS.tif"
    out_LSFACTOR = out_path + "out_LSFACTOR.tif"
    out_CHANNELS = out_path + "out_CHANNELS.tif"
    out_BASINS = out_path + "out_BASINS.tif"
    out_CHNL_BASE = out_path + "out_CHNL_BASE.tif"
    out_CHNL_DIST = out_path + "out_CHNL_DIST.tif"
    out_VALL_DEPTH = out_path + "out_VALL_DEPTH.tif"
    out_RSP = out_path + "out_RSP.tif"

    cmd = 'saga_cmd ta_compound 0 -ELEVATION ' + in_ELEVATION + ' -SHADE ' + out_SHADE+ ' -SLOPE ' + out_SLOPE + ' -HCURV ' + out_HCURV + ' -VCURV ' + out_VCURV + ' -CONVERGENCE ' + out_CONVERGENCE+ ' -SINKS ' + out_SINKS+ ' -CAREA ' + out_CAREA+ ' -WETNESS ' + out_WETNESS+ ' -LSFACTOR ' + out_LSFACTOR+ ' -CHANNELS ' + out_CHANNELS+ ' -BASINS ' + out_BASINS+ ' -CHNL_BASE ' + out_CHNL_BASE+ ' -CHNL_DIST ' + out_CHNL_DIST+ ' -VALL_DEPTH ' + out_VALL_DEPTH+ ' -RSP ' + out_RSP + ' -THRESHOLD 5' #+ out_THRESHOLD 
    
    try:
        runCommand_logged(cmd, logstd, logerr)
    except Exception, e:
        logerr.write("Exception thrown")
        logerr.write("ERROR: %s\n" % e)


saga_compound(dem_in ,out_path)

print "done"
