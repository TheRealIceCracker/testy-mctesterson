import zipfile
import sys

#def find

TECH_SCORE_MULTIPLIER = 10
ACCUMULATED_ENERGY_MULTIPLIER = 0.1
ACCUMULATED_MINERALS_MULTIPLIER = 0.05
ACCUMULATED_INFLUENCE_MULTIPLIER = 0.05
ENERGY_PRODUCTION_MULTIPLIER = 2
MINERAL_PRODUCTION_MULTIPLIER = 1.5
INFLUENCE_PRODUCTION_MULTIPLIER = 1
NUM_SUBJECTS_MULTIPLIER = 30
MILITARYPOWER_MULTIPLIER = 0.03
NUM_COLONIES_MULTIPLIER = 15
NUM_PLANETS_MULTIPLIER = 0.01

class Country:

    def __init__(self, s):
        self.name = ''
        self.s = s
        self.score = 0
        self.techscore = 0
        self.currentenergy = 0
        self.currentminerals = 0
        self.currentinfluence = 0
        self.energyproduction = 0
        self.mineralproduction = 0
        self.influenceproduction = 0
        self.numsubjects = 0
        self.militarypower = 0
        self.numcolonies = 0
        self.numplanets = 0
        self.init()
        self.calcscore()

    def calcscore(self):
        self.score += TECH_SCORE_MULTIPLIER * self.techscore
        self.score += ACCUMULATED_ENERGY_MULTIPLIER * self.currentenergy
        self.score += ACCUMULATED_MINERALS_MULTIPLIER * self.currentminerals
        self.score += ACCUMULATED_INFLUENCE_MULTIPLIER * self.currentinfluence
        self.score += ENERGY_PRODUCTION_MULTIPLIER * self.energyproduction
        self.score += MINERAL_PRODUCTION_MULTIPLIER * self.mineralproduction
        self.score += INFLUENCE_PRODUCTION_MULTIPLIER * self.influenceproduction
        self.score += NUM_SUBJECTS_MULTIPLIER * self.numsubjects
        self.score += MILITARYPOWER_MULTIPLIER * self.militarypower
        self.score += NUM_COLONIES_MULTIPLIER * self.numcolonies
        self.score += NUM_PLANETS_MULTIPLIER * self.numplanets
        
        
    def init(self):
        def checkn(k, n, m):
            return k[0:n+len(m)] == '\t'*n+m
        kt = self.s.split('\n')
        mode = 0
        
        for k2 in range(len(kt)):
            k = kt[k2]
            if (checkn(k, 2, 'name=')):
                self.name = k[k.find('"')+1:k.rfind('"')]
            elif (checkn(k, 3, 'technology=')):
                kk = kt[k2+1]
                if (checkn(kk, 3, 'level=')):
                    self.techscore += int(kk[kk.find('=')+1:])
            elif (checkn(k, 2, 'modules=')):
                mode = 1 # MODULE MODE
            elif (checkn(k, 3, 'standard_economy_module=')):
                mode = 2
            elif (mode == 2 and checkn(k, 4, 'resources=')):
                mode = 3
            elif (mode == 3 and checkn(k, 5, 'energy=')):
                self.currentenergy = float(k[k.find('=')+1:].replace('{', '').replace('}', '').split(' ')[0])
            elif (mode == 3 and checkn(k, 5, 'minerals=')):
                self.currentminerals = float(k[k.find('=')+1:].replace('{', '').replace('}', '').split(' ')[0])
            elif (mode == 3 and checkn(k, 5, 'influence=')):
                self.currentinfluence = float(k[k.find('=')+1:].replace('{', '').replace('}', '').split(' ')[0])
            elif (mode == 2 and checkn(k, 4, 'last_month=')):
                mode = 2.5
            elif (mode == 2.5 and checkn(k, 5, 'energy=')):
                
                self.energyproduction = float(k[k.find('=')+1:].replace('{', '').replace('}', '').split(' ')[0])
            elif (mode == 2.5 and checkn(k, 5, 'minerals=')):
                self.mineralproduction = float(k[k.find('=')+1:].replace('{', '').replace('}', '').split(' ')[0])
            elif (mode == 2.5 and checkn(k, 5, 'influence=')):
                self.influenceproduction = float(k[k.find('=')+1:].replace('{', '').replace('}', '').split(' ')[0])
            elif (checkn(k, 2, 'subjects=')):
                kk = kt[k2+1].strip()
                if kk != '}':
                    self.numsubjects = len(kk.split(' '))
            elif (checkn(k, 2, 'military_power=')):
                self.militarypower = float(k[k.find('=')+1:])
            elif (checkn(k, 2, 'owned_planets=')):
                kk = kt[k2+1].strip()
                if kk != '}':
                    self.numcolonies = len(kk.split(' '))
            elif (checkn(k, 2, 'controlled_planets=')):
                kk = kt[k2+1].strip()
                if kk != '}':
                    self.numplanets = len(kk.split(' '))
            
            elif (k.strip() == '}' and mode == 3):
                mode -= 1

zf = 'C:/Python33/stellarisscorechecker/2204.01.07.sav'
def ttt():
    save = zipfile.ZipFile(zf)
    f = save.open('gamestate')
    s = str(f.read(), 'utf-8')
    f.close()

    countries = s[s.find('country={'):]

    t = 1

    cdata = []
    csdata = ''
    for i in range(len('country={') + 1, len(countries)):
        if countries[i] == '{':
            if (t == 1):
                csdata = ''
                k = countries[i-1]
                j = i-1
                while(k != '\t'):
                    csdata = k + csdata
                    j -= 1
                    k = countries[j]
            t += 1
        elif countries[i] == '}':
            t -= 1
            if (t == 1):
                cdata.append(csdata + '}')
        csdata += countries[i]
        if (t == 0):
            countries = countries[:i+1]
            break
    

    cntrs = []

    
    for i in cdata:
        c = Country(i)
        cntrs.append(c)
    csv = 'Name,Score,Number of Known Techs,Military Power,Number of Colonies,Number of Planets,Number of Subject Nations,Accumulated Energy,Accumulated Minerals,Accumulated Influence,Energy Production,Minerals Production,Influence Production\n'
    for c in cntrs:
        csv += str(c.name) + ','
        csv += str(c.score) + ','
        csv += str(c.techscore) + ','
        csv += str(c.militarypower) + ','
        csv += str(c.numcolonies) + ','
        csv += str(c.numplanets) + ','
        csv += str(c.numsubjects) + ','
        csv += str(c.currentenergy) + ','
        csv += str(c.currentminerals) + ','
        csv += str(c.currentinfluence) + ','
        csv += str(c.energyproduction) + ','
        csv += str(c.mineralproduction) + ','
        csv += str(c.influenceproduction) + ','
        csv += '\n'
        print('---------------------')
        print(c.name)
        print("Score:", c.score, '---- Rank:', len([0 for v in cntrs if v.score > c.score])+1)
        print("Number of Known Techs:", c.techscore, '---- Rank:', len([0 for v in cntrs if v.techscore > c.techscore])+1)
        print("Military Power:", c.militarypower, '---- Rank:', len([0 for v in cntrs if v.militarypower > c.militarypower])+1)
        print("Number of Colonies:", c.numcolonies, '---- Rank:', len([0 for v in cntrs if v.numcolonies > c.numcolonies])+1)
        print("Number of Planets:", c.numplanets, '---- Rank:', len([0 for v in cntrs if v.numplanets > c.numplanets])+1)
        print("Number of Subject Nations:", c.numsubjects, '---- Rank:', len([0 for v in cntrs if v.numsubjects > c.numsubjects])+1)
        print("Accumulated Energy:", c.currentenergy, '---- Rank:', len([0 for v in cntrs if v.currentenergy > c.currentenergy])+1)
        print("Accumulated Minerals:", c.currentminerals, '---- Rank:', len([0 for v in cntrs if v.currentminerals > c.currentminerals])+1)
        print("Accumulated Influence:", c.currentinfluence, '---- Rank:', len([0 for v in cntrs if v.currentinfluence > c.currentinfluence])+1)
        print("Energy Production:", c.energyproduction, '---- Rank:', len([0 for v in cntrs if v.energyproduction > c.energyproduction])+1)
        print("Minerals Production:", c.mineralproduction, '---- Rank:', len([0 for v in cntrs if v.mineralproduction > c.mineralproduction])+1)
        print("Influence Production:", c.influenceproduction, '---- Rank:', len([0 for v in cntrs if v.influenceproduction > c.influenceproduction])+1)
        print('---------------------')

    fs = zf[:zf.rfind('.')] + '.csv'
    ttf = open(fs, 'w')
    ttf.write(csv)
    ttf.close()

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        zf = sys.argv[1]
        ttt()
        input()
    else:
        ttt()
    


