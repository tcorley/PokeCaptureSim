#!/etc/bin/ python
# Pokemon capture code

from random import randint
from sys import maxint, argv
from PIL import Image
import random
from bisect import bisect
import os, sys
from time import sleep

directory = os.path.dirname(os.path.abspath(__file__))

# greyscale.. the following strings represent
# 7 tonal ranges, from lighter to darker.
# for a given pixel tonal level, choose a character
# at random from that range.

greyscale = [
			" ",
			" ",
			".,-",
			"_ivc=!/|\\~",
			"gjez2]/(YL)t[+T7Vf",
			"mdK4ZGbNDXY5P*Q",
			"W8KMA",
			"#%$"
			]
 
# using the bisect class to put luminosity values
# in various ranges.
# these are the luminosity cut-off points for each
# of the 7 tonal levels. At the moment, these are 7 bands
# of even width, but they could be changed to boost
# contrast or change gamma, for example.
 
zonebounds=[36,72,108,144,180,216,252]
 
# open image and resize
# experiment with aspect ratios according to font
# Constants
VERBOSE = True

gen1 = ['Bulbasaur','Ivysaur','Venusaur','Charmander','Charmeleon','Charizard','Squirtle','Wartortle','Blastoise','Caterpie','Metapod','Butterfree','Weedle','Kakuna','Beedrill','Pidgey','Pidgeotto','Pidgeot','Rattata','Raticate','Spearow','Fearow','Ekans','Arbok','Pikachu','Raichu','Sandshrew','Sandslash','Nidoran','Nidorina','Nidoqueen','Nidoran','Nidorino','Nidoking','Clefairy','Clefable','Vulpix','Ninetales','Jigglypuff','Wigglytuff','Zubat','Golbat','Oddish','Gloom','Vileplume','Paras','Parasect','Venonat','Venomoth','Diglett','Dugtrio','Meowth','Persian','Psyduck','Golduck','Mankey','Primeape','Growlithe','Arcanine','Poliwag','Poliwhirl','Poliwrath','Abra','Kadabra','Alakazam','Machop','Machoke','Machamp','Bellsprout','Weepinbell','Victreebel','Tentacool','Tentacruel','Geodude','Graveler','Golem','Ponyta','Rapidash','Slowpoke','Slowbro','Magnemite','Magneton','Farfetch\'d','Doduo','Dodrio','Seel','Dewgong','Grimer','Muk','Shellder','Cloyster','Gastly','Haunter','Gengar','Onix','Drowzee','Hypno','Krabby','Kingler','Voltorb','Electrode','Exeggcute','Exeggutor','Cubone','Marowak','Hitmonlee','Hitmonchan','Lickitung','Koffing','Weezing','Rhyhorn','Rhydon','Chansey','Tangela','Kangaskhan','Horsea','Seadra','Goldeen','Seaking','Staryu','Starmie','Mr. Mime','Scyther','Jynx','Electabuzz','Magmar','Pinsir','Tauros','Magikarp','Gyarados','Lapras','Ditto','Eevee','Vaporeon','Jolteon','Flareon','Porygon','Omanyte','Omastar','Kabuto','Kabutops','Aerodactyl','Snorlax','Articuno','Zapdos','Moltres','Dratini','Dragonair','Dragonite','Mewtwo','Mew']
# Not all pokemon have catch rates, as they all cannot be caught in the wild. 
catchRate = { 'Caterpie' : 255, 'Metapod' : 120, 'Butterfree' : 45, 'Weedle' : 255, 'Kakuna' : 120, 'Beedrill' : 45, 'Pidgey' : 255, 'Pidgeotto' : 120, 'Rattata' : 255, 'Raticate' : 127, 'Spearow' : 255, 'Fearow' : 90, 'Ekans' : 255, 'Arbok' : 90, 'Pikachu' : 190, 'Sandshrew' : 255, 'Sandslash' : 90, 'Nidoran' : 235, 'Nidorina' : 120, 'Nidoran' : 235, 'Nidorino' : 120, 'Clefairy' : 150, 'Vulpix' : 190, 'Jigglypuff' : 170, 'Zubat' : 255, 'Golbat' : 90, 'Oddish' : 255, 'Gloom' : 120, 'Paras' : 190, 'Parasect' : 75, 'Venonat' : 190, 'Venomoth' : 75, 'Diglett' : 255, 'Dugtrio' : 50, 'Meowth' : 255, 'Persian' : 90, 'Psyduck' : 190, 'Golduck' : 75, 'Mankey' : 190, 'Primeape' : 75, 'Growlithe' : 190, 'Poliwag' : 255, 'Poliwhirl' : 120, 'Poliwrath' : 45, 'Abra' : 200, 'Kadabra' : 100, 'Machop' : 180, 'Machoke' : 90, 'Bellsprout' : 255, 'Weepinbell' : 120, 'Tentacool' : 190, 'Tentacruel' : 60, 'Geodude' : 255, 'Graveler' : 120, 'Ponyta' : 190, 'Rapidash' : 60, 'Slowpoke' : 190, 'Slowbro' : 75, 'Magnemite' : 190, 'Magneton' : 60, 'Farfetch\'d' : 45, 'Doduo' : 190, 'Dodrio' : 45, 'Seel' : 190, 'Dewgong' : 75, 'Grimer' : 190, 'Muk' : 75, 'Shellder' : 190, 'Gastly' : 190, 'Haunter' : 90, 'Gengar' : 45, 'Onix' : 45, 'Drowzee' : 190, 'Hypno' : 75, 'Krabby' : 225, 'Kingler' : 60, 'Voltorb' : 190, 'Electrode' : 120, 'Exeggcute' : 90, 'Exeggutor' : 45, 'Cubone' : 190, 'Marowak' : 75, 'Hitmonlee' : 45, 'Hitmonchan' : 45, 'Lickitung' : 45, 'Koffing' : 190, 'Weezing' : 60, 'Rhyhorn' : 120, 'Rhydon' : 60, 'Chansey' : 30, 'Tangela' : 45, 'Kangaskhan' : 45, 'Horsea' : 225, 'Seadra' : 75, 'Goldeen' : 225, 'Seaking' : 60, 'Staryu' : 225, 'Starmie' : 60, 'Mr. Mime' : 45, 'Scyther' : 45, 'Jynx' : 45, 'Electabuzz' : 45, 'Magmar' : 45, 'Pinsir' : 45, 'Tauros' : 45, 'Magikarp' : 255, 'Gyarados' : 45, 'Lapras' : 45, 'Ditto' : 35, 'Eevee' : 45, 'Porygon' : 45, 'Snorlax' : 25, 'Articuno' : 3, 'Zapdos' : 3, 'Moltres' : 3, 'Dratini' : 45, 'Dragonair' : 45, 'Dragonite' : 45, 'Mewtwo' : 3, 'Mew' : 45  }


# Pokeball Constants
def getBallVal(ball):
	return {
		'poke'  : randint(0,255),
		'great' : randint(0,200),
		'master': maxint
			}.get(ball, randint(0,150))

class Ailment():
	def __init__(self):
		choice = randint(0,3)
		if choice == 0:
			self.ailment = random.choice(['asleep','frozen'])
			self.catchThesh = 25
		elif choice == 1:
			self.ailment = random.choice(['paralyzed','burned','poisoned'])
			self.catchThesh = 12
		else:
			self.ailment = 'healthy'
			self.catchThresh = 0
	def getAilment(self):
		return self.ailment
	def getThresh(self):
		return self.catchThesh

class Conditions():
	def __init__(self,pokemon):
		self.health = randint(1,100)
		self.ailment = Ailment().getAilment()
		self.name = pokemon
		self.captureRate = catchRate.get(pokemon,100)

	def printConditions(self):
		print 'Health is at %d.'%self.health
		print 'Opponent is currently %s.'%self.ailment if not self.ailment == 'none' else 'Opponent has no status ailments.'

class Inventory():
	def __init__(self, difficulty):
		if difficulty == 'easy':
			# make array in the next iteration
			self.masterball =  1
			self.pokeball   =  20
			self.greatball  =  20
			self.ultraball  =  20
		
		else:
			self.masterball =  0
			self.pokeball   =  5
			self.greatball  =  5
			self.ultraball  =  5

	def printInventory(self):
		print '%d: %s: (%d)'%(1,'masterball',self.masterball)
		print '%d: %s: (%d)'%(2,'pokeball',self.pokeball)
		print '%d: %s: (%d)'%(3,'greatball',self.greatball)
		print '%d: %s: (%d)'%(4,'ultraball',self.ultraball)

	def getBallAmountFromValue(self,value):
		return {
			1 : self.masterball,
			2 : self.pokeball,
			3 : self.greatball,
			4 : self.ultraball
		}
	
	def removeBall(self, choice):
		if choice == 1:
			print 'Ash threw a Masterball!'
			self.masterball -= 1
		elif choice == 2:
			print 'Ash threw a pokeball!'
			self.pokeball -= 1
		elif choice == 3:
			print 'Ash threw a greatball!'
			self.greatball -= 1
		elif choice == 4:
			print 'Ash threw an ultraball!'
			self.ultraball -= 1
		else:
			print 'how did you even let this happen?'
			exit(1)
			



	# confusion is not taken into account for value
	

def main():
	print '**********************POKEMON CAPTURE SIMULATOR***************************'
	sleep(1)

	correctChoice = False
	choice = 'easy'
	# while not correctChoice:
	# 	choice = raw_input("Easy, or hard? ").lower()
	# 	correctChoice = choice.find('easy') >= 0 or choice.find('hard') >= 0

	balls = Inventory(choice)

	balls.printInventory()

	pokemon = gen1[randint(0,len(gen1)-1)]
	# pokemon = catchRate.keys().pop(randint(0,len(catchRate)-1))
	print '%s\nA wild %s appeared!' % (drawASCII(gen1.index(pokemon)+1),pokemon)
	sleep(1)
	print '\n<battle ensues>'
	# for time in xrange(1,10):
	# 	sys.stdout.write('.')
	# 	sleep(.5)

	opponent = Conditions(pokemon)
	opponent.printConditions()

	balls.printInventory()

	choiceCheck = False
	choice = 0
	while not choiceCheck:
		choice = int(raw_input('Select number of pokeball to throw! '))
		choiceCheck = choice >= 1 and choice <= 4 and balls.getBallAmountFromValue(choice) > 0
		if not choiceCheck:
			print 'Incorrect entry. Try again'

	balls.removeBall(choice)

	if capture(opponent, choice):
		print 'Congratulations! you caught a %s!\n'%pokemon
		choosy = int(raw_input('Catch another?: '))
		if choosy == 1:
			main()
		else: 
			exit(0)
	else:
		print 'Fuck! %s broke free!'%pokemon
		sleep(1)
		print '%s fled!'%pokemon
		return 


def capture(opponent, pokeball):
	if pokeball == 1:
		#no computation needed for a master ball
		print '<shake left>'
		sleep(1)
		print '<shake right>'
		sleep(1)
		print '<shake left>'
		sleep(1)
		print '***click***'
		sleep(1)
		return True
	return False





def drawASCII(num):
	# im=Image.open(r"/Users/Tyler_iMac/Downloads/Sprites/151.png")
	#im=Image.open(r"/Users/Tyler_iMac/Downloads/Sprites/%03d.png"%num)
	file = os.path.join(directory, 'sprites', '%03d.png'%num)
	im = Image.open(file)
	# im=im.resize((n+85, n),Image.BILINEAR)
	# im=im.resize((40, 19),Image.BILINEAR)
	im=im.resize((104, 70),Image.BILINEAR)
	im=im.convert("L") # convert to mono
	 
	# now, work our way over the pixels
	# build up str
	 
	str=""
	for y in range(0,im.size[1]):
		for x in range(0,im.size[0]):
			lum=255-im.getpixel((x,y))
			row=bisect(zonebounds,lum)
			possibles=greyscale[row]
			str=str+possibles[random.randint(0,len(possibles)-1)]
		str=str+"\n"
	 
	checkString = str.split('\n')
	for string in checkString:
		if(string.isspace()):
			checkString.pop(checkString.index(string))
	return '\n'.join(checkString)


if __name__ == "__main__":
	main()

