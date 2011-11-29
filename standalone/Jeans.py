#!/usr/bin/env python
# Jeans.py
# Jeans Foundation #4
# Designer: Helen Joseph-Armstrong
# PatternMaker: Susan Spencer Conklin
#
# This pattern contains a design for a pair of jeans

from tmtpl.constants import *
from tmtpl.pattern import *
from tmtpl.document import *
from tmtpl.client import Client
from tmtpl.curves import GetCurveControlPoints,  myGetControlPoints

#Project specific
#from math import sin, cos, radians
from math import sqrt

from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *


class PatternDesign():

	def __init__(self):
		self.styledefs={}
		self.markerdefs={}
		return

	def pattern(self):
		"""
		Method defining a pattern design. This is where the designer places
		all elements of the design definition
		"""
		CM=CM_TO_PX
		IN=IN_TO_PX
		#The following attributes are set before calling this method:
		#self.cd - Client Data, which has been loaded from the client data file
		#self.styledefs - the style difinition dictionary, loaded from the styles file
		#self.markerdefs - the marker definition dictionary
		#self.cfg - configuration settings from the main app framework
		#TODO - find a way to get this administrative cruft out of this pattern method
		cd=self.cd	#client data is prefaced with cd.
		self.cfg['clientdata']=cd
		#TODO - also extract these from this file to somewhere else
		printer='36" wide carriage plotter'
		if (printer=='36" wide carriage plotter'):
		    self.cfg['paper_width']=(36 * IN)
		self.cfg['border']=(5*CM)#document borders
		BORDER=self.cfg['border']
		#self.cfg['verbose']=('')#debug statements
		BORDER=self.cfg['border']
		# 1:  womens=W, mens=M, teensgirls=TG, teenboys=TB, girls=G, boys=B, toddlers=T, babies=B, crafts=C
		# 2:  streetwearable=S, period=P, fantasy=F
		# 3:  3digit year: 1870:870, 880, 890,900,910,920,930,940,950,960,970,980,990,000,010
		# 4:    none=x, Gaming=g, Futuristic=f, Cosplay=c, GothLolita=g, Military=m, BasicCostumes=c
		# 5: dress=d, pants=p, jeans=j, shirt/blouse=s, tshirt=t, jacket=j, coat=c, vest=v, hat=h, pjs=p, lingerie=l, swimsuits=s,
		#  ....maternity=m, accessories=a
		# 6: casual=1, elegant=2, day&evening=3, grunge&skate=4, sports=5
		# 7: followed by Absolute Number of patterns generated
		#TODO - abstract these into configuration file(s)
		metainfo={'companyName':'Seamly Patterns',  #mandatory
					'designerName':'Susan Spencer',#mandatory
					'patternName':'Jeans Foundation',#mandatory
					'patternNumber':'WS010-xj1-1' #mandatory
					}
		self.cfg['metainfo']=metainfo
		#attributes for the entire svg document
		docattrs={'currentscale' : "0.5 : 1",
					'fitBoxtoViewport' : "True",
					'preserveAspectRatio' : "xMidYMid meet",
					}
		doc=Document(self.cfg, name='document', attributes=docattrs)
		#Set up the Title Block and Test Grid for the top of the document
		TB=TitleBlock('notes', 'titleblock', 0, 0, stylename='titleblock_text_style')
		doc.add(TB)
		TG=TestGrid('notes', 'testgrid', self.cfg['paper_width']/3.0, 0, stylename='cuttingline_style')
		doc.add(TG)

		#client & pattern measurements
		FRONTWAISTARC=(cd.front_waist_width/2.0)
		FRONTABDOMENARC=(cd.front_abdomen_width/2.0)
		FRONTHIPARC=(cd.front_hip_width/2.0)
		BACKWAISTARC=(cd.back_waist_width/2.0)
		BACKABDOMENARC=(cd.back_abdomen_width/2.0)
		BACKHIPARC=(cd.back_hip_width/2.0)

		WAISTLINE=(1.0*IN) # Jeans waist is 1" lower than actual waist
		ABDOMENLINE=WAISTLINE + cd.front_abdomen_height
		RISELINE=WAISTLINE + cd.rise
		HIPLINE=WAISTLINE + (2/3.0)*(RISELINE)
		HEMLINE=WAISTLINE + cd.outside_leg
		KNEELINE=RISELINE+(abs(HEMLINE-RISELINE)/2.0)-(1.0*IN)

		WAISTBAND=(1.0*IN) # Height of Waistband

		if ((FRONTHIPARC-FRONTWAISTARC)>= (2.0*IN)):
			FRONTNORMALWAIST=1
		else:
			FRONTNORMALWAIST=0

		if ((BACKHIPARC-BACKWAISTARC)>= (2.0*IN)):
			BACKNORMALWAIST=1
		else:
			BACKNORMALWAIST=0

		#Begin Jeans Pattern Set
		jeans=Pattern('jeans')
		doc.add(jeans)
		jeans.styledefs.update(self.styledefs)
		jeans.markerdefs.update(self.markerdefs)

		# Jeans Front 'A'
		jeans.add(PatternPiece('pattern', 'front', letter='A', fabric=2, interfacing=0, lining=0))
		A=jeans.front
		ASTART=0.0
		AEND=(FRONTHIPARC+((1/8.0)*IN))
		AStart=rPoint(A, 'AStart', ASTART, ASTART)
		AEnd=rPoint(A, 'AEnd', AEND, ASTART)
		AWaist=rPoint(A, 'AWaist', ASTART, WAISTLINE)
		AAbdomen=rPoint(A, 'AAbdomen', ASTART, ABDOMENLINE)
		AHip=rPoint(A, 'AHip', ASTART, HIPLINE)
		ARise=rPoint(A, 'ARise', ASTART, RISELINE)

		Ap1=rPoint(A, 'Ap1', AEND, WAISTLINE) # right side of reference grid
		Ap5=rPoint(A, 'Ap5', AEND/2.0, WAISTLINE) # dart midpoint
		Ap6=rPoint(A, 'Ap6', Ap5.x-(.25*IN), WAISTLINE) #dart outside leg (left on pattern)
		Ap7=rPoint(A, 'Ap7', Ap5.x+(.25*IN), WAISTLINE) # dart inside leg (right on pattern)
		Ap8=rPoint(A, 'Ap8', Ap5.x, Ap5.y+(2.5*IN)) # dart point
		Ap2=rPoint(A, 'Ap2', Ap7.x+(FRONTWAISTARC/2.0), WAISTLINE)
		Ap3=rPoint(A, 'Ap3', Ap2.x, WAISTLINE-(0.25)*IN) # center waist
		Ap4=rPoint(A, 'Ap4', Ap6.x-(FRONTWAISTARC/2.0), WAISTLINE) # side waist
		Ap9=rPoint(A, 'Ap9', AEND, (RISELINE/2.0)) # center front 'pivot' point from crotch curve to front fly
		Ap10=rPoint(A, 'Ap10', ASTART, HIPLINE)
		Ap11=rPoint(A, 'Ap11', AEND, HIPLINE)
		Ap12=rPoint(A, 'Ap12', ASTART, RISELINE)
		Ap13=rPoint(A, 'Ap13', AEND, RISELINE)
		Ap14=rPointP(A, 'Ap14', pntFromDistanceAndAngleP(Ap13, (1.25*IN), angleFromSlope(1.0, 1.0))) # inside crotch curve point
		Ap15=rPoint(A, 'Ap15', Ap13.x+(2.0*IN), RISELINE) # point of crotch
		Ap16=rPoint(A, 'Ap16', Ap15.x/2.0, RISELINE) # creaseline point
		Ap17=rPoint(A, 'Ap17', Ap16.x, KNEELINE)
		Ap18=rPoint(A, 'Ap18', Ap16.x-(4.0*IN), KNEELINE) # outside knee
		Ap19=rPoint(A, 'Ap19', Ap16.x+(4.0*IN), KNEELINE) # inside knee
		Ap20=rPoint(A, 'Ap20', Ap16.x, HEMLINE)
		Ap21=rPoint(A, 'Ap21', Ap20.x-(3.5*IN), HEMLINE) # outside hem
		Ap22=rPoint(A, 'Ap22', Ap20.x+(3.5*IN), HEMLINE) # inside hem
		Ap23=rPoint(A, 'Ap23', Ap8.x-(FRONTABDOMENARC/2.0), ABDOMENLINE)
		Ap24=rPoint(A, 'Ap24', Ap8.x+(FRONTABDOMENARC/2.0), ABDOMENLINE)

		# front waist AW
		AW1=rPointP(A,'AW1', Ap3) # center waist
		AW2=rPointP(A, 'AW2', pntIntersectLinesP(Ap3, Ap4, Ap8, Ap7)) # inside dart at waist
		AW4=rPointP(A, 'AW4', pntOnLineP(Ap8, Ap6, lineLengthP(Ap8, AW2))) # outside dart at waist
		angle1=angleP(Ap7, Ap8) # angle of  inside dart leg
		angle2=angleP(Ap8, Ap6) # angle of outside dart leg
		angle3=angle2 - angle1 # angle of entire dart
		angle=angle1 - angle3 # actual angle of back fold of dart after bringing outside-leg to meet inside-leg then folding to the center ??? should be to side..# TODO change this
		pnt=pntIntersectLinesP(Ap8, pntFromDistanceAndAngleP(Ap8, lineLengthP(Ap8, Ap7), angle), AW1, AW2)
		AW3=rPointP(A, 'AW3', pntOnLineP(Ap8, Ap5, lineLengthP(Ap8, pnt)) ) # midpoint dart at waist
		AW5=rPointP(A, 'AW5', Ap4) # side waist
		#front waist control points
		distance=(lineLengthP(AW4, AW5)/3.0)
		cAW5b=cPoint(A, 'cAW5b', AW5.x+distance, AW5.y)
		cAW5a=cPointP(A, 'cAW5a', pntOnLineP(AW4, cAW5b, distance))

		# front dart point AD
		AD1=rPointP(A, 'AD1', Ap8) # point of dart
		AD2=rPoint(A, 'AD2', AW3.x, AW3.y - (5/8.0)*IN) #midpoint of dart legs
		AD3=rPointP(A, 'AD3', pntIntersectLines(AW4.x, AW4.y-(5/8.0)*IN, AW5.x, AW5.y-(5/8.0)*IN, Ap8.x, Ap8.y, AW4.x, AW4.y)) # outside dart leg
		AD4=rPointP(A, 'AD4', pntIntersectLines(AW1.x, AW1.y-(5/8.0)*IN, AW2.x, AW2.y-(5/8.0)*IN, Ap8.x, Ap8.y, AW2.x, AW2.y)) #inside dart leg

		# front side seam AS
		AS1=rPointP(A, 'AS1', Ap10)
		AS2=rPointP(A, 'AS2', Ap12)
		AS3=rPointP(A, 'AS3', Ap18)
		AS4=rPointP(A, 'AS4', Ap21)
		# front side seam control points
		if (FRONTNORMALWAIST):
			cAS3b=cPointP(A, 'cAS3b', pntOffLineP(AS3, AS4, (lineLengthP(AS3, AS1)/2.0))) # b/w AS1 & AS3
			pnts=pointList(AW5, AS1, AS3)
			c1, c2=myGetControlPoints('FrontSideSeam', pnts)
			cAS1a=cPoint(A, 'cAS1a', c1[0].x, c1[0].y) #b/w AW5 & AS2
			cAS1b=cPoint(A, 'cAS1b', AS1.x, c2[0].y) #b/w AW5 & AS1
			cAS3a=cPoint(A, 'cAS3a', AS1.x, c1[1].y) #b/w AS1 & AW5
		else:
			cAS2a=cPoint(A, 'cAS2a', min(AS2.x, AW5.x), AW5.y+(lineLengthP(AW5, AS2)/3.0)) # waistline slightly less than hipline (ex: 1.25") use AS2 else AW5
			cAS3b=cPointP(A, 'cAS3b', pntOffLineP(AS3, AS4, (lineLengthP(AS2, AS3)/3.0))) # b/w AS2 & AS3
			pnts=pointList(cAS2a, AS2, cAS3b)
			fcp, scp=myGetControlPoints('BackSideSeam', pnts)
			cAS2b=cPoint(A, 'cAS2b', scp[0].x, scp[0].y) #b/w AW5 & AS2
			cAS3a=cPoint(A, 'cAS3a', fcp[1].x, fcp[1].y) #b/w AS2 & AS3

		# front inseam AI
		AI1=rPointP(A, 'AI1', Ap22)
		AI2=rPointP(A, 'AI2', Ap19)
		AI3=rPointP(A, 'AI3', Ap15)
		#front inseam control points
		cAI3a=cPointP(A, 'cAI3a', pntOffLineP(AI2, AI1, (lineLengthP(AI2, AI3)/2.0))) #b/w AI2 & AI3
		cAI3b=cPointP(A, 'cAI3b', pntOnLineP(AI3, cAI3a, (lineLengthP(AI2, AI3)/3.0))) #b/w AI2 & AI3

		#front center seam AC
		AC1=rPointP(A, 'AC1', Ap14)
		if (FRONTNORMALWAIST):
			AC2=rPointP(A, 'AC2', Ap9)
			# straight line for upper front center seam, control points for AC1 & AC2 only, with calculated control point cAC2b to smooth into straight line
			cAC2b=cPointP(A, 'cAC2b', pntOffLine(AC2.x, AC2.y, AW1.x, AW1.y, (lineLengthP(AC1, AC2)/2.0)))
			pnts=pointList(AI3, AC1, cAC2b)
			fcp, scp=myGetControlPoints('FrontCenterSeam', pnts)
			cAC1a=cPoint(A, 'cAC1a', fcp[0].x, fcp[0].y) #b/w AI3 & AC1
			cAC1b=cPoint(A, 'cAC1b', scp[0].x, scp[0].y) #b/w AI3 & AC1
			cAC2a=cPoint(A, 'cAC2a', fcp[1].x, fcp[1].y) #b/w AC1 & AC2
		else:
			# cubic curve for entire front center seam
			AC2=rPoint(A, 'AC2', Ap9.x + (abs(FRONTHIPARC-FRONTWAISTARC)/4.0), Ap9.y)
			cAC2a=cPointP(A, 'cAC2a', pntOnLineP(AC1, Ap13, (lineLengthP(AI3, Ap13)/4.0))) #b/w AI3 & AC2
			cAC2b=cPointP(A, 'cAC2b', pntOffLineP(AC2, AW1, (lineLengthP(AC2, AW1)/3.0))) #b/w AI3 & AC2

		# points to create Jeans Waistband pattern 'C'
		Ap25=rPointP(A, 'Ap25', pntOnLineP(AW1, AC2, WAISTBAND)) # waistband below center waist
		if FRONTNORMALWAIST:
			pnt=pntOnLineP(AW5, cAS1a, WAISTBAND)
		else:
			pnt=pntOnLineP(AW5, cAS2a, WAISTBAND)
		Ap28=rPointP(A, 'Ap28', pnt) # waistband line 1in. below side waist
		Ap26=rPointP(A, 'Ap26', pntIntersectLinesP(Ap25, Ap28, Ap8, Ap7)) # waistband line at inside dart leg
		Ap27=rPointP(A, 'Ap27', pntIntersectLinesP(Ap25, Ap28, Ap8, Ap6)) # waistband line at outside dart leg

		#front grainline AG & label location
		AG1=rPoint(A, 'AG1', Ap16.x, HIPLINE)
		AG2=rPoint(A, 'AG2', Ap16.x, Ap18.y+abs(Ap21.y-Ap18.y)/2.0)
		(A.label_x, A.label_y)=(AG2.x, AG2.y-(2.0*IN))

		#grid 'Agrid' path
		Agrid=path()
		#   vertical Agrid
		addToPath(Agrid, 'M', AStart, 'L', ARise, 'M', Ap5, 'L', Ap8, 'M', Ap16, 'L', Ap20, 'M', Ap3, 'L', Ap2, 'M', AEnd, 'L', Ap13)
		#   horizontal Agridid
		addToPath(Agrid, 'M', AStart, 'L', AEnd, 'M', AWaist, 'L', Ap1, 'M', Ap23, 'L', Ap24, 'M', AHip, 'L', Ap11, 'M', ARise, 'L', Ap15, 'M', Ap18, 'L', Ap19, 'M', Ap25, 'L', Ap26, 'M', Ap27, 'L', Ap28)
		#   diagonal grid
		addToPath(Agrid, 'M', Ap3, 'L', Ap4, 'M', Ap13, 'L', Ap14)
		# dart 'd' path
		d=path()
		addToPath(d, 'M', AD1, 'L', AD2, 'M', AD3, 'L', AD1, 'L', AD4)
		# seamline 's' & cuttingline 'c' paths
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			addToPath(p, 'M', AW1,  'L', AW2, 'L', AW3, 'L', AW4, 'C', cAW5a,  cAW5b,  AW5)
			if (FRONTNORMALWAIST):
				addToPath(p, 'C', cAS1a, cAS1b, AS1)
			else:
				addToPath(p, 'C', cAS2a, cAS2b, AS2)
			addToPath(p, 'C', cAS3a, cAS3b, AS3, 'L', AS4, 'L', AI1, 'L',  AI2, 'C', cAI3a, cAI3b, AI3)
			if (FRONTNORMALWAIST):
				cubicCurveP(p, cAC1a, cAC1b, AC1)
			addToPath(p, 'C', cAC2a, cAC2b, AC2, 'L',  AW1)

		# add grainline, dart, seamline & cuttingline paths to pattern
		A.add(grainLinePath("grainLine", "Jeans Front Grainline", AG1, AG2))
		A.add(Path('reference','grid', 'Jeans Front Gridline', Agrid, 'gridline_style'))
		A.add(Path('pattern', 'dartline', 'Jeans Front Dartline', d, 'dart_style'))
		A.add(Path('pattern', 'seamLine', 'Jeans Front Seamline', s, 'seamline_path_style'))
		A.add(Path('pattern', 'cuttingLine', 'Jeans Front Cuttingline', c, 'cuttingline_style'))

		# Jeans Back 'B'
		jeans.add(PatternPiece('pattern', 'back', letter='B', fabric=2, interfacing=0, lining=0))
		B=jeans.back
		BSTART=0.0
		BEND=((1.25)*BACKHIPARC)
		BStart=rPoint(B, 'BStart', BSTART, BSTART)
		BEnd=rPoint(B, 'BEnd', BEND, BSTART)
		BWaist=rPoint(B, 'BWaist', BSTART, WAISTLINE)
		BAbdomen=rPoint(B, 'BAbdomen', BSTART, ABDOMENLINE)
		BHip=rPoint(B, 'BHip', BSTART, HIPLINE)
		BRise=rPoint(B, 'BRise', BSTART, RISELINE)
		Bp1=rPoint(B, 'Bp1', BSTART+((0.25)*BACKHIPARC), WAISTLINE)
		Bp2=rPoint(B, 'Bp2', BEND, WAISTLINE)
		Bp5=rPoint(B, 'Bp5', Bp1.x+((BEND-Bp1.x)/2.0), WAISTLINE)
		Bp6=rPoint(B, 'Bp6', Bp5.x-((3/8.0)*IN), WAISTLINE)
		Bp7=rPoint(B, 'Bp7', Bp5.x + ((3/8.0)*IN), WAISTLINE)
		Bp8=rPoint(B, 'Bp8', Bp5.x, (Bp5.y + (3.5*IN) ) )
		if (BACKNORMALWAIST):
			Bp3=rPoint(B, 'Bp3', Bp1.x+(1.75*IN), WAISTLINE)
			Bp4=rPoint(B, 'Bp4', Bp1.x+(BACKWAISTARC)+(1.0*IN), WAISTLINE)
		else:
			Bp3=rPoint(B, 'Bp3', Bp6.x-(BACKWAISTARC/2.0)-((1/8)*IN), WAISTLINE)
			Bp4=rPoint(B, 'Bp4', Bp7.x+(BACKWAISTARC/2.0)+((1/8)*IN), WAISTLINE)
		Bp9=rPoint(B, 'Bp9', Bp1.x, HIPLINE-(abs(RISELINE-HIPLINE)/2.0))
		Bp10=rPoint(B, 'Bp10', Bp1.x, HIPLINE)
		Bp11=rPoint(B, 'Bp11', Bp2.x, HIPLINE)
		Bp12=rPoint(B, 'Bp12', BStart.x, RISELINE)
		Bp13=rPoint(B, 'Bp13', Bp1.x, RISELINE)
		Bp14=rPointP(B, 'Bp14', pntFromDistanceAndAngleP(Bp13, (1.75*IN), angleFromSlope(1.0, -1.0)))
		Bp15=rPoint(B, 'Bp15', Bp2.x, RISELINE)
		Bp16=rPoint(B, 'Bp16', Bp15.x-((3./8.0)*IN), RISELINE)
		Bp17=rPoint(B, 'Bp17',(Bp16.x-Bp12.x)/2., RISELINE)
		Bp18=rPoint(B, 'Bp18', Bp17.x, KNEELINE)
		Bp19=rPoint(B, 'Bp19', Bp18.x-(4.50*IN), KNEELINE)
		Bp20=rPoint(B, 'Bp20', Bp18.x+(4.50*IN), KNEELINE)
		Bp21=rPoint(B, 'Bp21', Bp18.x, HEMLINE)
		Bp22=rPoint(B, 'Bp22', Bp21.x-(4.*IN), HEMLINE)
		Bp23=rPoint(B, 'Bp23', Bp21.x+(4.*IN), HEMLINE)
		Bp24=rPoint(B, 'Bp24', Bp8.x-(BACKABDOMENARC/2.0)-((1/8.0)*IN), ABDOMENLINE)
		Bp25=rPoint(B, 'Bp25', Bp8.x+(BACKABDOMENARC/2.0)+((1/8.0)*IN), ABDOMENLINE)

		# back waist
		BW1=rPoint(B,'BW1', Bp3.x, BStart.y)
		BW2=rPointP(B, 'BW2', pntIntersectLinesP(BW1, Bp4, Bp8, Bp6))
		angle1=angleP(Bp8, Bp6) # actual angle of left-leg line of dart
		angle2=angleP(Bp8, Bp7) # actual angle of right-leg line of dart
		angle3=(angle1 - angle2) # absolute angle of entire dart -->  left leg - right leg
		angle=angle1 + angle3 # actual angle of back fold of dart after bringing right-leg of dart to meet left-leg & folding to the left (towards center seam)
		pnt1=pntFromDistanceAndAngleP(Bp8, lineLengthP(Bp8, Bp6), angle)
		pnt2=pntIntersectLinesP(Bp8, pnt1, BW1, BW2)
		BW3=rPointP(B, 'BW3', pntOnLineP(Bp8, Bp5, lineLengthP(Bp8, pnt2)))
		BW4=rPointP(B, 'BW4', pntOnLineP(Bp8, Bp7, lineLengthP(Bp8, BW2)))
		BW5=rPointP(B, 'BW5', Bp4)
		# back waist control points
		distance=(lineLengthP(BW4, BW5)/3.0)
		cBW5b=cPoint(B, 'cBW5b', BW5.x-distance, BW5.y)
		cBW5a=cPointP(B, 'cBW5a', pntOnLineP(BW4, cBW5b, distance))

		#back dart
		BD1=rPointP(B, 'BD1', Bp8)
		BD2=rPoint(B, 'BD2', BW3.x, BW3.y - (5/8.0)*IN)
		BD3=rPointP(B, 'BD3', pntIntersectLines(BW4.x, BW4.y-(5/8.0)*IN, BW5.x, BW5.y-(5/8.0)*IN, Bp8.x, Bp8.y, BW4.x, BW4.y))
		BD4=rPointP(B, 'BD4', pntIntersectLines(BW1.x, BW1.y-(5/8.0)*IN, BW2.x, BW2.y-(5/8.0)*IN, Bp8.x, Bp8.y, BW2.x, BW2.y))

		#back side seam
		BS1=rPointP(B, 'BS1', Bp11)
		BS2=rPointP(B, 'BS2', Bp15)
		BS3=rPointP(B, 'BS3', Bp20)
		BS4=rPointP(B, 'BS4', Bp23)
		if (BACKNORMALWAIST):
			cBS3b=cPointP(B, 'cBS3b', pntOffLineP(BS3, BS4, (lineLengthP(BS3, BS1)/2.0))) # b/w BS1 & BS3
			pnts=pointList(BW5, BS1, BS3)
			c1, c2=myGetControlPoints('BackSideSeam', pnts)
			cBS1a=cPoint(B, 'cBS1a', c1[0].x, c1[0].y) #b/w BW5 & BS2
			cBS1b=cPoint(B, 'cBS1b', BS1.x, c2[0].y) #b/w BW5 & BS1
			cBS3a=cPoint(B, 'cBS3a', BS1.x, c1[1].y) #b/w BS1 & BW5
		else:
			cBS2a=cPoint(B, 'cBS2a', BW5.x, BW5.y+(lineLengthP(BW5, BS2)/3.0))
			cBS3b=cPointP(B, 'cBS3b', pntOffLineP(BS3, BS4, (lineLengthP(BS2, BS3)/3.0))) # b/w BS2 & BS3
			pnts=pointList(cBS2a, BS2, cBS3b)
			fcp, scp=myGetControlPoints('BackSideSeam', pnts)
			cBS2b=cPoint(B, 'cBS2b', scp[0].x, scp[0].y) #b/w BW5 & BS2
			cBS3a=cPoint(B, 'cBS3a', fcp[1].x, fcp[1].y) #b/w BS2 & BS3

		# back inseam
		BI1=rPointP(B, 'BI1', Bp22)
		BI2=rPointP(B, 'BI2', Bp19)
		BI3=rPointP(B, 'BI3', Bp12)
		distance=(lineLengthP(BI2, BI3)/3.0)
		cBI3a=cPointP(B, 'cBI3a', pntOffLineP(BI2, BI1, distance)) #b/w BI2 & BI3
		cBI3b=cPointP(B, 'cBI3b', pntOnLineP(BI3, cBI3a, distance)) #b/w BI2 & BI3

		#back center seam
		BC1=rPointP(B, 'BC1', Bp14)
		#back center seam control points
		if (BACKNORMALWAIST):
			BC2=rPointP(B, 'BC2', Bp9)
			# straight line for upper back center seam, control points for BC1 & BC2 only, with calculated control point for control point leading into straight line
			cBC2b=cPointP(B, 'cBC2b', pntOffLineP(BC2, BW1, (lineLengthP(BC1, BC2)/3.0)))
			pnts=pointList(BI3, BC1, cBC2b)
			fcp, scp=myGetControlPoints('BackCenterSeam', pnts)
			cBC1a=cPoint(B, 'cBC1a', fcp[0].x, fcp[0].y) #b/w BI3 & BC1
			cBC1b=cPoint(B, 'cBC1b', scp[0].x, scp[0].y) #b/w BI3 & BC1
			cBC2a=cPoint(B, 'cBC2a', fcp[1].x, fcp[1].y) #b/w BC1 & BC2
		else:
			BC2=rPoint(B, 'BC2', Bp9.x-(abs(BACKHIPARC-BACKWAISTARC)/4.0), Bp9.y)
			cBC2a=cPointP(B, 'cBC2a', pntOnLineP(BC1, Bp13, (lineLengthP(BI3, Bp13)/4.0))) #b/w BI3 & BC2
			cBC2b=cPointP(B, 'cBC2b', pntOffLineP(BC2, BW1, (lineLengthP(BC2, BW1)/3.0))) #b/w BI3 & BC2

		# back points to create Jeans Waistband pattern 'C'
		Bp26=rPointP(B, 'Bp26', pntOnLineP(BW1, BC2, WAISTBAND)) # waistband below center waist
		if BACKNORMALWAIST:
			pnt=pntOnLineP(BW5, cBS1a, WAISTBAND)
		else:
			pnt=pntOnLineP(BW5, cBS2a, WAISTBAND)
		Bp29=rPointP(B, 'Bp29', pnt) # waistband line 1in. below side waist
		Bp27=rPointP(B, 'Bp27', pntIntersectLinesP(Bp26, Bp29, Bp8, Bp6)) # waistband line at inside dart leg
		Bp28=rPointP(B, 'Bp28', pntIntersectLinesP(Bp26, Bp29, Bp8, Bp7)) # waistband line at outside dart leg

		#back grainline & label location
		BG1=rPoint(B, 'BG1', Bp17.x, HIPLINE)
		BG2=rPoint(B, 'BG2', BG1.x, Bp18.y+(Bp21.y-Bp18.y)/2.0)
		(B.label_x, B.label_y)=(BG2.x, BG2.y-(2.0*IN))

		#grid 'Bgrid' path
		Bgrid=path()
		#   vertical grid
		addToPath(Bgrid, 'M', BStart, 'L', BRise, 'M', Bp1, 'L', Bp13, 'M', BEnd, 'L', Bp15, 'M', Bp17, 'L', Bp21, 'M', Bp5, 'L', Bp8)
		#   horizontal grid
		addToPath(Bgrid, 'M', BStart, 'L', BEnd, 'M', BWaist, 'L', Bp2, 'M', BHip, 'L', Bp11, 'M', BRise, 'L', Bp15, 'M', Bp19, 'L', Bp20)
		#   diagonal grid
		addToPath(Bgrid, 'M', BW1, 'L', BW5, 'M', Bp13, 'L', Bp14)
		#dart 'd' path
		d=path()
		addToPath(d, 'M', BD1, 'L', BD2, 'M', BD3, 'L', BD1, 'L', BD4)
		#seamline 's' & cuttingline 'c' paths
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			addToPath(p, 'M', BW1, 'L', BW2, 'L', BW3, 'L', BW4, 'C', cBW5a, cBW5b, BW5)
			if (BACKNORMALWAIST):
				addToPath(p, 'C', cBS1a, cBS1b, BS1)
			else:
				addToPath(p, 'C', cBS2a, cBS2b, BS2)
			addToPath(p, 'C', cBS3a, cBS3b, BS3, 'L', BS4, 'L', BI1, 'L', BI2, 'C', cBI3a, cBI3b, BI3)
			if (BACKNORMALWAIST):
				addToPath(p, 'C', cBC1a, cBC1b, BC1)
			addToPath(p, 'C', cBC2a, cBC2b, BC2, 'L', BW1)
		# add grid, dart, grainline, seamline & cuttingline paths to pattern
		B.add(grainLinePath("grainLine", "Jeans Back Grainline", BG1, BG2))
		B.add(Path('reference','Bgrid', 'Trousers Back Gridline', Bgrid, 'gridline_style'))
		B.add(Path('pattern', 'dartline', 'Jeans Back Dartline', d, 'dart_style'))
		B.add(Path('pattern', 'seamLine', 'Jeans Back Seamline', s, 'seamline_path_style'))
		B.add(Path('pattern', 'cuttingLine', 'Jeans Back Cuttingline', c, 'cuttingline_style'))

		# Jeans Waistband 'C'
		jeans.add(PatternPiece('pattern', 'LeftWaistband', letter='C', fabric=2, interfacing=1, lining=0))
		C=jeans.LeftWaistband
		CSTART=0.0
		CEND=(FRONTWAISTARC+BACKWAISTARC)
		CStart=rPoint(C, 'CStart', BSTART, BSTART)
		CEnd=rPoint(C, 'CEnd', BEND, BSTART)

		CX1=rPoint(C,'CX1', Ap28.x, Ap28.y-WAISTBAND) # reference point to center the waistband

		connector0=Ap28 #object1..front waistband,center section, right side, low...Ap28 <===> Ap28 (connector2)...no change
		connector1=CX1 # object1...point vertical from Ap28...CX1<===> AW5 ...straightens up 1st object
		connector2=Ap28 #object2...front waistband,side section, left side, low
		connector3=AW1  #object2...front waistband,side section, left side, high
		connector_pnts=pointList(connector0, connector1, connector2, connector3)
		old_pnts=pointList(Ap28, AW5, AW4, Ap27) # front waistband, side section old points
		new_pnts=connectObjects(connector_pnts, old_pnts) # front waistband, side section new points
		C8=rPoint(C, 'C8', new_pnts[0].x, new_pnts[0].y)
		C3=rPoint(C, 'C3', new_pnts[1].x, new_pnts[1].y)
		C2=rPoint(C, 'C2', new_pnts[2].x, new_pnts[2].y)
		C9=rPoint(C, 'C9', new_pnts[3].x, new_pnts[3].y)

		connector0=Ap28 #object1..Ap28 <===> Bp29
		connector1=CX1 #object1...CX1 <===> BW5
		connector2=Bp29 #object2...back waistband,side section, right side, low
		connector3=BW5  #object2...back waistband,side section, right side, high
		connector_pnts=pointList(connector0, connector1, connector2, connector3)
		old_pnts=pointList(Bp29, BW5, BW4, Bp28) # front waistband, side section old points
		new_pnts=connectObjects(connector_pnts, old_pnts) # front waistband, side section new points
		# new_pnts[0] =C8 ( on lower edge of waistband), new_pnts[1] =C3 (on upper edge)
		C4=rPoint(C, 'C4', new_pnts[2].x, new_pnts[2].y)
		C7=rPoint(C, 'C7', new_pnts[3].x, new_pnts[3].y)

		connector0=C9 #object2...front waistband,side section,right side, low...C9 <===> Ap26
		connector1=C2 #object2...front waistband,side section,right side, high...C2<===> AW2
		connector2=Ap26 #object3...front waistband,center section,right side,low
		connector3=AW2 #object3...front waistband,center section,right side,high
		connector_pnts=pointList(connector0, connector1, connector2, connector3)
		old_pnts=pointList(Ap26, AW2, AW1, Ap25)
		new_pnts=connectObjects(connector_pnts, old_pnts)
		C1=rPoint(C, 'C1', new_pnts[2].x, new_pnts[2].y)
		C10=rPoint(C, 'C10', new_pnts[3].x, new_pnts[3].y)

		connector0=C7 #object3...back waistband,side section,left side, low...C7 <===> Bp27 (connector6)
		connector1=C4 #object3...front waistband,side section,left side, high...C4 <===> BW2 (connector7)
		connector2=Bp27 #object4...back waistband,center section,right side,low
		connector3=BW2 #object4...back waistband,center section,right side,high
		connector_pnts=pointList(connector0, connector1, connector2, connector3)
		old_pnts=pointList(Bp27, BW2, BW1, Bp26)
		new_pnts=connectObjects(connector_pnts, old_pnts)
		C5=rPoint(C, 'C5', new_pnts[2].x, new_pnts[2].y)
		C6=rPoint(C, 'C6', new_pnts[3].x, new_pnts[3].y)

		cC3a=cPointP(C, 'cC3a', pntOffLineP(C2, C1, lineLengthP(C2, C3)/3.0)) #b/w C2 & C3
		cC4b=cPointP(C, 'cC4b', pntOffLineP(C4, C5, lineLengthP(C4, C3)/3.0)) #b/w C4 & C3
		pnts=pointList(cC3a, C3, cC4b)
		c1, c2=myGetControlPoints('LeftWaistbandTopEdge', pnts)
		cC3b=cPointP(C, 'cC3b', pntOnLineP(C3, c2[0], lineLengthP(C2, C3)/3.0)) #b/w C2 & C3
		cC4a=cPointP(C, 'cC4a', pntOnLineP(C3, c1[1], lineLengthP(C4, C3)/3.0)) #b/w C4 & C3

		cC8a=cPointP(C, 'cC8a', pntOffLineP(C7, C6, lineLengthP(C7, C8)/3.0)) #b/w C7 & C8
		cC9b=cPointP(C, 'cC9b', pntOffLineP(C9, C10, lineLengthP(C9, C8)/3.0)) #b/w C9 & C8
		pnts=pointList(cC8a, C8, cC9b)
		c1, c2=myGetControlPoints('LeftWaistbandLowerEdge', pnts)
		cC8b=cPointP(C, 'cC8b', pntOnLineP(C8, c2[0], lineLengthP(C7, C8)/3.0)) #b/w C7 & C8
		cC9a=cPointP(C, 'cC9a', pntOnLineP(C8, c1[1], lineLengthP(C9, C8)/3.0)) #b/w C8 & C9

		#grainline points & label location
		CG1=rPoint(C, 'CG1', C2.x+(1.0*IN), C2.y + (0.5*IN))
		CG2=rPoint(C, 'CG2', CG1.x + (1.5*IN), CG1.y)
		(C.label_x, C.label_y)=(CG2.x, CG2.y)

		#grid 'Cgrid' path
		Cgrid=path()
		addToPath(Cgrid, 'M', C2, 'L', C9, 'M',C3,'L',C8,'M', C4, 'L', C7)

		# seamline 's' & cuttingline 'c' paths
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			addToPath(p, 'M', C1, 'L', C2, 'C', cC3a, cC3b, C3, 'C', cC4a, cC4b, C4, 'L', C5)
			addToPath(p, 'L', C6, 'L', C7, 'C', cC8a, cC8b, C8, 'C', cC9a, cC9b, C9, 'L', C10, 'L', C1)

		# add grainline, seamline & cuttingline paths to pattern
		C.add(grainLinePath("grainLine", "Left Waistband Grainline", CG1, CG2))
		C.add(Path('reference','grid', 'Left Waistband Reference Grid', Cgrid, 'gridline_style'))
		C.add(Path('pattern', 'seamLine', 'Left Waistband Seamline', s, 'seamline_path_style'))
		C.add(Path('pattern', 'cuttingLine', 'Left Waistband Cuttingline', c, 'cuttingline_style'))

		#call draw once for the entire pattern
		doc.draw()
		return

# vi:set ts=4 sw=4 expandtab:

