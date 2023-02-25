from wSVG import *


oSVG = wSVG("Acceleration_A320_Edinburg.csv", 0, 3)

oSVG.titleY = """Acceleration (m/s<tspan dy ="-1">2</tspan><tspan dy ="1">)</tspan>"""
oSVG.title = "Messung"
oSVG.outputXmax = 100
oSVG.outputYmin = 5
oSVG.outputYmax = 15

oSVG.renderToFile("wAusgabe.svg")
