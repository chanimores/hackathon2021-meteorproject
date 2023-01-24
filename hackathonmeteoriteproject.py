"""
HackathonMeteoriteProject.ipynb
File was originally created on Colaboratory.

## Meteorite Plotting Project

This project was created as part of the McGill Physics 2021 Hackathon.

The goal of the project was to create a interactive sphere with NASA meteorite data plotted onto it. 
The meteorite landing data was extracted from a csv file containing geolocation data.

Link to the hackathon project page: https://devpost.com/software/meteorite-plotting-project

"""

import plotly as ply
import numpy as np
import pandas as pd

# Plot the Sphere

# Creates the coordinates for thes phere
theta = np.linspace(0,2*np.pi,100)
phi = np.linspace(0,np.pi,100)
x = np.outer(np.cos(theta),np.sin(phi))
y = np.outer(np.sin(theta),np.sin(phi))
z = np.outer(np.ones(100),np.cos(phi))

# Creates the sphere surface
data = ply.graph_objs.Surface(x=x, y=y, z=z, colorscale='teal', contours=ply.graph_objs.surface.Contours(
        x=ply.graph_objs.surface.contours.X(highlight=False),
        y=ply.graph_objs.surface.contours.Y(highlight=False),
        z=ply.graph_objs.surface.contours.Z(highlight=False),
    ))

# Remove axes
noaxis=dict(showbackground=False,
    showgrid=False,
    showline=False,
    showticklabels=False,
    ticks='',
    title='',
    zeroline=False)

# Set-up graph layout
layout = ply.graph_objs.Layout(
    title='Graph of Earth with Meteorite Landings plotted',
    autosize = False,
    width=650,
    height=650,
    showlegend = False,
    scene = dict(
        xaxis = noaxis,
        yaxis = noaxis,
        zaxis = noaxis,
        aspectmode='manual',
        aspectratio=ply.graph_objs.layout.scene.Aspectratio(x=1, y=1, z=1)),
    paper_bgcolor = 'grey',
    plot_bgcolor = 'grey',
    hovermode=False
)


# Add sphere to the graph and remove colorscale
fig = ply.graph_objs.Figure(data=data, layout=layout)

# Imports Data from file here

# Opens file
filename = "Meteorite_Landings.csv"
file_obj = open(filename, "r")

# x, y should be lists
x, y = [], []

# Reads through the whole file line by line
for line in file_obj.readlines():

    # Splits lines by commas (as it is a CSV file)
    newlines = line.split(",")

    # Get geolocation data
    x_temp, y_temp = newlines[9], newlines[10]

    # Convert to float and store in x, y lists
    try: 
        x_temp = float(x_temp)
        y_temp = float(y_temp)

        x.append(float(x_temp))
        y.append(float(y_temp))

    # Throws an error if the value is not a float (NaN or empty)
    except ValueError: 
        pass
  
file_obj.close()

# Converts the geolocation data from degree to radians for plotting

# Sets to keep converted data
x_conv, y_conv, z_conv = [],[],[]

length_of_set = len(x)

# Iterate through each x, y from the set and convert it into radians
for i in range(0, length_of_set):
    x_temp = x.pop() * np.pi/180
    y_temp = y.pop() * np.pi/180
  
    # Append new x, y, z values to the data sets
    x_conv.append(1.07 * np.sin(y_temp)*np.sin(x_temp))
    y_conv.append(1.07 * np.cos(x_temp))
    z_conv.append(1.07 * np.cos(y_temp)* np.sin(x_temp))

# Plot Data Points onto Sphere via coordinates

import plotly.express as px

# Remove color scale
fig.update_traces(showscale=False)

# Set data from points
d = {'x': x_conv, 'y':y_conv, 'z': z_conv}
df = pd.DataFrame(data=d)

# Add to graph
fig.add_scatter3d(name='points', x=df['x'], y=df['y'], z=df['z'], mode="markers",
                  marker=dict(size=1.5, color='palegreen'))

fig.update_layout(dict(width=1500, height=700),
        scene = dict(
            xaxis = dict(visible=False),
            yaxis = dict(visible=False),
            zaxis =dict(visible=False)
        ))

# Show Graph (for testing purposes)
#fig.show()

# Export the graph to an html page
ply.offline.plot(fig, validate = False, filename='index.html', auto_open=True)