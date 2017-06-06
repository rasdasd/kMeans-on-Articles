#plot functions
#latitude	longitude	title	date	topic
import plotly.offline as py
import plotly.graph_objs as go

def plotLatLongOnMap(data_dict):
	scl = [ [0,"rgb(5, 10, 172)"] ]
	data = [ dict(
		type = 'scattergeo',
		#locationmode = 'USA-states',
		lon = data_dict['longitude'],
		lat = data_dict['latitude'],
		text = data_dict['topic'],
		mode = 'markers',
		marker = dict(
			size = 8,
			opacity = 0.8,
			reversescale = True,
			autocolorscale = False,
			symbol = 'square',
			line = dict(
				width=1,
				color='rgba(102, 102, 102)'
			),
			colorscale = scl,
			cmin = 0,
			color = 0,
			cmax = 0
		))]

	layout = dict(
			title = 'Scatter Plot of News Articles',
			colorbar = True,
			geo = dict(
				#scope='usa',
				#projection=dict( type='albers usa' ),
				showland = True,
				landcolor = "rgb(250, 250, 250)",
				subunitcolor = "rgb(217, 217, 217)",
				countrycolor = "rgb(217, 217, 217)",
				countrywidth = 0.5,
				subunitwidth = 0.5
			),
		)

	fig = dict( data=data, layout=layout )

	py.plot( fig, validate=False, filename='charts/scatter-plot.html' )

def plotScatterOverTime(cluster_centers_list, weekCount):
	# plot articles as regular data over time
	scl = [ [0,"rgb(5, 10, 172)"] ]
	data = []
	for i in range(weekCount):
		trace_points = go.Scattergeo(
			visible = False,
			type = 'scattergeo',
			showlegend = True,
			name = 'Articles: ' + cluster_centers_list['date_range'][i],
			#locationmode = 'USA-states',
			lon = cluster_centers_list[i]['points']['lon'],
			lat = cluster_centers_list[i]['points']['lat'],
			text = cluster_centers_list[i]['points']['topic'],
			mode = 'markers',
			marker = dict(
				size = 8,
				opacity = 0.8,
				reversescale = True,
				autocolorscale = True,
				symbol = 'square',
				line = dict(
					width=1,
					color='rgba(102, 102, 102)'
				),
				colorscale = scl,
				cmin = 0,
				color = 0,
				cmax = 0
			))
		data.append(trace_points)
	data[-1].visible = True
	steps = []
	for i in range(weekCount):
		step = dict(
			method = 'restyle',
			args = ['visible', [False] * len(data)],
			label = list(range(weekCount))
		)
		step['args'][1][i] = True # Toggle i'th trace to "visible"
		steps.append(step)
	sliders = [dict(
		active = weekCount-1,
		currentvalue = {'prefix': 'Weeks Showing: '},
		pad = {'t': 1},
		steps = steps
		)]

	layout = dict(
			title = 'Scatter Plot Over Time',
			colorbar = True,
			showlegend=True,
			geo = dict(
				#scope='usa',
				#projection=dict( type='albers usa' ),
				showland = True,
				landcolor = "rgb(250, 250, 250)",
				subunitcolor = "rgb(217, 217, 217)",
				countrycolor = "rgb(217, 217, 217)",
				countrywidth = 0.5,
				subunitwidth = 0.5
			),
			sliders = sliders
		)

	fig = dict( data=data, layout=layout )

	py.plot( fig, validate=False, filename='charts/Scatter-Time.html' )



def plotDataCluster(data_dict,cluster_centers_list,closestClusterNumbers,weekCount):
	# data_dict, the parsed data dict
	# cluster_centers_list, the cluster centers in order, dict of lon and lat
	# closestClusterNumbers, in order, what point belongs to which cluster
	k = len(cluster_centers_list[weekCount-1]['lon'])
	data = []
	for i in range(weekCount):
		trace_points = go.Scattergeo(
			visible = False,
			type = 'scattergeo',
			showlegend = True,
			name = 'Articles: ' + cluster_centers_list['date_range'][i],
			#locationmode = 'USA-states',
			lon = cluster_centers_list[i]['points']['lon'],
			lat = cluster_centers_list[i]['points']['lat'],
			text = closestClusterNumbers[i],
			mode = 'markers',
			marker = dict(
				size = 8,
				opacity = 0.8,
				reversescale = True,
				autocolorscale = True,
				symbol = 'square',
				line = dict(
					width=1,
					color='rgba(102, 102, 102)'
				),
				cmin = 0,
				color = closestClusterNumbers[i],
				cmax = k
			))
		trace_hotspots = go.Scattergeo(
			visible = False,
			type = 'scattergeo',
			showlegend = True,
			name = 'Hotspots: ' + cluster_centers_list['date_range'][i],
			#locationmode = 'USA-states',
			lon = cluster_centers_list[i]['lon'],
			lat = cluster_centers_list[i]['lat'],
			text = list(range(k)),
			mode = 'markers',
			marker = dict(
				size = 20,
				opacity = 0.8,
				reversescale = True,
				autocolorscale = True,
				symbol = 'circle',
				line = dict(
					width=1,
					color='rgba(250, 20, 20)'
				),
				cmin = 0,
				color = list(range(k)),
				cmax = k
			))
		data.append(trace_points)
		data.append(trace_hotspots)
	data[-2].visible = True
	data[-1].visible = True
	steps = []
	for i in range(weekCount):
		step = dict(
			method = 'restyle',
			args = ['visible', [False] * len(data)],
			label = list(range(weekCount))
		)
		step['args'][1][2*i] = True # Toggle 2i'th trace to "visible"
		step['args'][1][(2*i)+1] = True # Toggle 2i+1'th trace to "visible"
		steps.append(step)
	sliders = [dict(
		active = weekCount-1,
		currentvalue = {'prefix': 'Weeks Showing: '},
		pad = {'t': 1},
		steps = steps
		)]

	layout = dict(
			title = 'K Means with k = '+str(k),
			colorbar = True,
			showlegend=True,
			geo = dict(
				#scope='usa',
				#projection=dict( type='albers usa' ),
				showland = True,
				landcolor = "rgb(250, 250, 250)",
				subunitcolor = "rgb(217, 217, 217)",
				countrycolor = "rgb(217, 217, 217)",
				countrywidth = 0.5,
				subunitwidth = 0.5
			),
			sliders = sliders
		)

	fig = dict( data=data, layout=layout )

	py.plot( fig, validate=False, filename='charts/kMeans.html' )

def plotElbowMethod(ks, sses):
	data = go.Scatter(
		x = ks,
		y = sses,
		mode = 'lines+markers',
		name = 'Elbow Method'
		)
	layout = go.Layout(
		title = 'Elbow Method'
		)
	fig = dict( data=[data], layout=layout )

	py.plot( fig, validate=False, filename='charts/elbow.html' )


def plotTfidf(dataset):
	#if not PLOT:
		#return
	# data_dict, the parsed data dict
	# cluster_centers_list, the cluster centers in order, dict of lon and lat
	# closestClusterNumbers, in order, what point belongs to which cluster
	weekCount = dataset['weekcount']
	k = len(dataset['cluster_centers'][weekCount-1]['lon'])
	data = []
	for w in range(weekCount):
		trace_points = go.Scattergeo(
			visible = False,
			type = 'scattergeo',
			showlegend = True,
			name = 'Articles: ' + dataset['cluster_centers']['date_range'][w],
			#locationmode = 'USA-states',
			lon = dataset['cluster_centers'][w]['points']['lon'],
			lat = dataset['cluster_centers'][w]['points']['lat'],
			text = dataset['article_strings'][w],
			mode = 'markers',
			marker = dict(
				size = 8,
				opacity = 0.8,
				reversescale = True,
				autocolorscale = True,
				symbol = 'square',
				line = dict(
					width=1,
					color='rgba(102, 102, 102)'
				),
				cmin = 0,
				color = dataset['cluster'][w],
				cmax = k
			))
		tracelist = go.Scattergeo(
			visible = False,
			type = 'scattergeo',
			showlegend = True,
			name = 'Hotspots: ' + dataset['cluster_centers']['date_range'][w],
			#locationmode = 'USA-states',
			lon = dataset['cluster_centers'][w]['lon'],
			lat = dataset['cluster_centers'][w]['lat'],
			text = dataset['cluster_strings'][w],
			mode = 'markers',
			marker = dict(
				size = 20,
				opacity = 0.8,
				reversescale = True,
				autocolorscale = True,
				symbol = 'circle',
				line = dict(
					width=1,
					color='rgba(250, 20, 20)'
				),
				cmin = 0,
				color = list(range(k)),
				cmax = k
			))
		data.append(trace_points)
		data.append(tracelist)

	data[-1].visible = True
	data[-2].visible = True
	
	steps = []
	for i in range(weekCount):
		step = dict(
			method = 'restyle',
			args = ['visible', [False] * len(data)],
			label = list(range(weekCount))
		)
		step['args'][1][2*i] = True # Toggle 2i'th trace to "visible"
		step['args'][1][(2*i)+1] = True # Toggle 2i+1'th trace to "visible"
		steps.append(step)
	sliders = [dict(
		active = weekCount-1,
		currentvalue = {'prefix': 'Weeks Showing: '},
		pad = {'t': 1},
		steps = steps
		)]

	layout = dict(
			title = 'tf-idf analysis on clusters',
			colorbar = True,
			showlegend=True,
			geo = dict(
				#scope='usa',
				#projection=dict( type='albers usa' ),
				showland = True,
				landcolor = "rgb(250, 250, 250)",
				subunitcolor = "rgb(217, 217, 217)",
				countrycolor = "rgb(217, 217, 217)",
				countrywidth = 0.5,
				subunitwidth = 0.5
			),
			sliders = sliders
		)

	fig = dict( data=data, layout=layout )

	py.plot( fig, validate=False, filename='charts/tfidf.html' )