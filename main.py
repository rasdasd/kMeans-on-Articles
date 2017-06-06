#primer take home
import plotUtil
import importData
import kMeansUtil
import exploreUtil
import numpy
def main():
	FILE = 'zika_latitude_longitude.tsv'

	#IMPORT DATA
	data = importData.importFile(FILE)
	#QUESTION ONE, PLOT DATA
	plotUtil.plotLatLongOnMap(data)
	#QUESTION TWO, cluster locations via k-means
	(cluster_centers, clusterNumbers, weekCount) = kMeansUtil.run(data)
	#Scatter over time, extra part for QUESTION ONE
	plotUtil.plotScatterOverTime(cluster_centers,weekCount)
	#QUESTION THREE, explore
	exploreUtil.explore(data,clusterNumbers, cluster_centers, weekCount)
	return data
data = ''
if __name__=="__main__":
	data = main()

