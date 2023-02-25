from csv import *

#
# SVG Generator designed for:    Kantonsschule Wattwil
#
#               This is a first darft. I'm eager to get some Feedback!
#               christoph.kendel........kantiwattwil.ch
#

class wSVG:
    titleX = "X"
    titleY = "Y"
    title  = "title"
    data = []
    dataNrLines = 0;
    dataXmin = float("NaN")
    dataXmax = float("NaN")
    dataYmin = float("NaN")
    dataYmax = float("NaN")
    dataYsumme = 0.0
    
    outputXmin = 0.0
    outputXmax = 300.0
    outputXtic = 20.0
    outputYmin = 0.0
    outputYmax = 20.0
    outputYtic = 1.0
    
    slidingAverageCount = 100

    def __init__(self, dataFileName="", columnX=0, columnY=1):
        if(dataFileName != ""):
            self.readFile(dataFileName, columnX, columnY)
       

    def renderToFile(self, fileName):
                
        s = self.startText
        s+= self.createTitleX()
        s+= self.createTitleY()
        s+= self.createTitle()
        s+= self.createGrid()
        s+= self.createDataPoints()
        s+= self.createSlidingAverage()
        s+= self.createNumbers()
        s+= self.finalText
        
        f = open(fileName, "w")
        f.write(s)
        f.close()    
    
    def readFile(self, dataFileName, columnX, columnY):
        f = open(dataFileName)
        fileCSV = reader(f)
        i = 0
        
        for rowCSV in fileCSV:
            i = i + 1
            if(i == 1):
                self.titleX = rowCSV[columnX]
                self.titleY = rowCSV[columnY]
                continue
            x =float(rowCSV[columnX])
            y =float(rowCSV[columnY])
            
            self.data.append([x,y])
            
            if(i == 2):
                self.dataXmin = x
                self.dataXmax = x
                self.dataYmin = y
                self.dataYmax = y
            if(x < self.dataXmin):
                self.dataXmin = x
            elif(x > self.dataXmax):
                self.dataXmax = x
            if(y < self.dataYmin):
                self.dataYmin = y
            elif(y > self.dataYmax):
                self.dataYmax = y
                
            self.dataYsumme += y
        f.close()
        self.dataNrLines = i
        print("Daten: X im Bereich von " + str(self.dataXmin) + " bis  " + str(self.dataXmax)  )
        print("Daten: Y im Bereich von " + str(self.dataYmin) + " bis  " + str(self.dataYmax)  )
        print("Eventuell anpassen mit oSVG.outputXmax = 300")
        
        
    def createDataPoints(self):
        scaleX = (143-6)/(self.outputXmax - self.outputXmin) # Usable X-Space:  6 >> 143
        scaleY = (12-94)/(self.outputYmax - self.outputYmin) # Usable Y-Space:  94 >> 12
        translateY = 94 - self.outputYmin * scaleY  

        # X-Y-Coordinates of this group equals the data-values. Scaling in x- and y- is done via the <g scale>
        s = """<g transform="translate(6.0 """+str(translateY)+""") scale(""" + str(scaleX) + " " + str(scaleY)+""")">\n"""
        for p in self.data:
            if(p[0] < self.outputXmax):
                s += '          <circle cx="'+str(p[0])+'" cy="'+str(p[1])+'" r="0.1" fill="black" />\n'
        s += "</g>\n\n"
        return s
    
    def createSlidingAverage(self):
        scaleX = (143-6)/(self.outputXmax - self.outputXmin) # Usable X-Space:  6 >> 143
        scaleY = (12-94)/(self.outputYmax - self.outputYmin) # Usable Y-Space:  94 >> 12
        translateY = 94 - self.outputYmin * scaleY  

        s = """<g transform="translate(6.0 """+str(translateY)+""") scale(""" + str(scaleX) + " " + str(scaleY)+""")">\n"""
        
        n = self.slidingAverageCount
        boxNr = 0
        p = " "
        while self.slidingAverageCount*(boxNr +1) < len(self.data): 
            a = 0.0
            for x in range(n):
                a += self.data[x + n*boxNr][1]
            yAverage = a / n
            if(boxNr == 1):
                p = " M " + str(self.data[int((n/2 + n*boxNr))][0])+" "+str(yAverage)
            elif(self.data[int((n/2 + n*boxNr))][0] < self.outputXmax):
                p += " L " + str(self.data[int((n/2 + n*boxNr))][0])+" "+str(yAverage)
            
            boxNr += 1
        return s+"""<path  stroke="blue" stroke-width="0.2"  fill="none" d='"""+p+"""' />""" + "</g>"
        
        
    def createGrid(self):
        scaleX = (143-6)/(self.outputXmax - self.outputXmin) # Usable X-Space:  6 >> 143
        scaleY = (12-94)/(self.outputYmax - self.outputYmin) # Usable Y-Space:  94 >> 12
        translateY = 94 - self.outputYmin * scaleY  
        
        s = """<g transform="translate(6.0 """+str(translateY)+""") scale(""" + str(scaleX) + " " + str(scaleY)+""")">\n"""
        n = 1
        while  self.outputXmin + n*self.outputXtic < self.outputXmax:
            s += """        <path
            style="fill:none;stroke:#cccccc;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
            d='M """ + str(self.outputXmin + n*self.outputXtic)+"," + str(self.outputYmin)+" "+ str(self.outputXmin + n*self.outputXtic)+"," + str(self.outputYmax)+"""'
            id="path875" />"""
            n += 1
        n = 1
        while  self.outputYmin + n*self.outputYtic < self.outputYmax:
            s += """        <path
            style="fill:none;stroke:#cccccc;stroke-width:0.03;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
            d='M """ + str(self.outputXmin)+"," + str(self.outputYmin + n*self.outputYtic)+" "+ str(self.outputXmax)+"," + str(self.outputYmin + n*self.outputYtic)+"""'
            id="path874" />"""
            n += 1
            
        s += "</g>\n\n"
        return s
    
    def createNumbers(self):
        scaleX = (143-6)/(self.outputXmax - self.outputXmin) # Usable X-Space:  6 >> 143
        scaleY = (12-94)/(self.outputYmax - self.outputYmin) # Usable Y-Space:  94 >> 12
        translateY = 94 - self.outputYmin * scaleY  
        s = "<g>"
        n = 0
        # X Tics
        while  self.outputXmin + n*self.outputXtic < (self.outputXmax - 10):
            x = (self.outputXmin + n*self.outputXtic)
            s += self.createOneNumber(x*scaleX + 4, self.outputYmin * scaleY + translateY + 4 , int(x+0.5))
            n += 1
        n = 0
        # Y Tics
        while  self.outputYmin + n*self.outputYtic < (self.outputYmax - 3):
            y = (self.outputYmin + n*self.outputYtic)
            s += self.createOneNumber(3, (self.outputYmin + n*self.outputYtic) * scaleY + translateY , int(y+0.5))
            n += 1
        s += "</g>"
        return s
    
    def createOneNumber(self, x, y, nr):
        s = """<text  xml:space="preserve"  id="text19"> <tspan  style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:3px;font-family:'Times New Roman';stroke-width:0.264583"
            x='""" + str(x)+ """' y='"""+str(y)+"""' id="tspan17">"""+str(nr)+"""</tspan></text>"""
        return s
    
    def createTitleX(self):
        return self.createText(self.titleX, 130, 100, 0)
    
    def createTitleY(self):
        return self.createText(self.titleY, -42, 4, -90)
    
    def createTitle(self):
        return self.createText(self.title, 58, 7, 0)
        
    def createText(self, text, x, y, orientation):
    	return """<text
           xml:space="preserve" """ \
            + ("> " if (orientation==0) else (""" transform="rotate("""+str(orientation)+""")">"""))\
            + """<tspan 
             style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:4.93889px;font-family:'Times New Roman';stroke-width:0.264583"
             x=" """+str(x)+""" "
             y=" """+str(y)+""" ">"""+text+"""</tspan></text>
        """
             
    finalText = "\n</svg>"
      
    startText = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!-- Created with wSVG (http://www.kantiwattwil.ch/) based on InkScape -->
    
    <svg
       width="149mm"
       height="105mm"
       viewBox="0 0 149 105"
       version="1.1"
       id="svg5"
       xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker
           style="overflow:visible"
           id="Arrow5"
           refX="0"
           refY="0"
           orient="auto-start-reverse"
           markerWidth="5.8"
           markerHeight="6.6"
           viewBox="0 0 5.8 6.6">
          <path
             transform="scale(0.8)"
             style="fill:context-stroke;fill-rule:evenodd;stroke:context-stroke;stroke-width:1pt"
             d="m 6,0 c -3,1 -7,3 -9,5 0,0 0,-4 2,-5 -2,-1 -2,-5 -2,-5 2,2 6,4 9,5 z" />
        </marker>
      </defs>
         <path
           style="fill:none;stroke:#000000;stroke-width:0.312199px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;marker-end:url(#Arrow5)"
           d="M 6.0,98 V 10.0"  id="path5650" />
        <path
           style="fill:none;stroke:#000000;stroke-width:0.376931px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;marker-end:url(#Arrow5)"
           d="M 3.0,94.0 H 140" id="path5651" />
        """
	