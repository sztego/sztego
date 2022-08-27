from random import randint
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Player:
    def __init__(self,name,max_hp,hp,gold,min_dmg,max_dmg,\
                 bonus_dmg,xp_max,xp,level,roomID):
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.gold = gold
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.bonus_dmg = bonus_dmg
        self.xp_max = xp_max
        self.xp = xp
        self.level = level
        self.roomID = roomID

class Monster:
    def __init__(self,name,max_hp,hp,min_dmg,max_dmg,xp,gold):
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.xp = xp
        self.gold = gold

class Tile:
    def __init__(self,name,x,y):
        self.name = name
        self.x = x
        self.y = y

class Room(Tile):
    def __init__(self,name,x,y,event):
        super().__init__(name,x,y)
        self.event = event

monsters = []
def monster_add ():
    monsters.append(Monster("Ork",5,5,3,5,5,3))
    monsters.append(Monster("Goblin",3,3,1,4,3,5))
    monsters.append(Monster("Nyálka",10,10,1,2,5,0))
    monsters.append(Monster("Ögre",8,8,5,8,10,4))
    monsters.append(Monster("Zombi",10,10,1,4,6,1))
                    
                    
def menu ():
    print("Ez itt főmenü.")
    print("Két választásod van: ")
    a = str(input("Új játékot kezdessz (1) vagy kilépsz a játékból (2)"))
    while a not in ("1","2"):
        print("Mondom 1 vagy 2!")
        a = str(input("Új játékot kezdessz (1) vagy kilépsz a játékból (2)"))
    return a

events = ["entrance","exit","trap","chest","monster"]
tiles = []
rooms = []
def generate_map(w,h):
    for i in range(w):
        for j in range(h):
            tiles.append(Tile("tile_"+str(i*6+j+1),i+1,j+1))

    rooms.append(Room("room_1",1,1,events[0]))
    while rooms[len(rooms)-1].x < w :
        room_tiles = []
        for i in range(1,len(tiles)):
            if (tiles[i].x == rooms[len(rooms)-1].x and tiles[i].y == rooms[len(rooms)-1].y+1) \
               or (tiles[i].x == rooms[len(rooms)-1].x+1 and tiles[i].y == rooms[len(rooms)-1].y):
                room_tiles.append(tiles[i])

        next_room = room_tiles[randint(0,len(room_tiles)-1)]
        rooms.append(Room("room_"+str(len(rooms)+1),next_room.x,next_room.y,events[randint(2,4)]))
        if rooms[len(rooms)-1].x == w:
            rooms[len(rooms)-1].event = events[1]
        
def data (p):
    print("")
    print("Az x="+str(rooms[p.roomID].x)\
          +" y="+str(rooms[p.roomID].y)+" helyen állsz.")
    print(str(p.gold)+" aranyad van.")
    print(str(p.hp)+"/"+str(p.max_hp)+" életed van.")
    print(str(p.xp)+"/"+str(p.xp_max)+" tapasztalati pontod van.")
    print("A sebzésed 2-4 + "+str(p.bonus_dmg)+".")
    print("")
    
def healer (a):
    while a.hp < a.max_hp and a.gold >= 7:
            print("")
            print("Az orrod előtt a levegőben hirtelen megjelent a jó tündér.")
            print("Látom megsérültél, szeretnéd hogy meggyógyítsalak?")
            print("7 aranyért megteszem.")
            gyogyit = input("(i/n)")
            if gyogyit not in ("i","n"):
                print("")
                print("Mondom i vagy n!")
                continue
            elif gyogyit == "i":
                a.hp = a.max_hp
                a.gold -= 7
                data(a)
                break
            else:
                print("Ha nem, hát nem.")
                data(a)
                break

def sleep(p):
    print("")
    print("Elmentél aludni egyet")
    print("Gyógyultál 50%-ot, de cserében vesztettél 2 xp-t,")
    print("mert felejtettél abból amit eddig tanultál.")
    p.hp = min(p.hp + int(p.max_hp * 0.5),p.max_hp)
    p.xp = max(p.xp - 2,0)

def roads(p):
    while player.hp > 0:
        data(player)
        healer(player)
        print("")
        print("Sötét alagút tátong előtted.")
        ut = str(input("Tovább mész (1), vagy inkább lefekszel aludni?(2)"))
        cls()
        if ut not in ("1","2"):
            print("")
            print("Mondom 1 vagy 2!")
            continue
        if ut == "2":
            sleep(p)
        else:
            p.roomID += 1
            if rooms[p.roomID].event == "exit":
                print("")
                print("Ügyes voltál, átjutottál a szűk folyosókon.")
                print("A barlang itt kiszélesedik, majd egy lezárt ajtóban végződik.")
                print("Az ajtót feltörve a nap sugara csillan a fegyvereden.")
                print("Visszaértél a külvilágba.")
                print("Gratulálok, megnyerted a játékot!")
                break
            if rooms[p.roomID].event == "trap":
                sebzodes = randint(1,5)
                p.hp -= sebzodes
                print("")
                print("Figyelmetlen voltál, csapdába léptél. Sebződtél "+str(sebzodes)+"-t.")
                print("")
                if p.hp <= 0:
                    print("Meghaltál, vége a játéknak.")
                    print("Játszunk legközelebb is!")
                    break
            elif rooms[p.roomID].event == "gold":
                zsakmany = randint(1,8)
                p.gold += zsakmany
                print("")
                print("Mázlid van: találtál egy kincsesládát, benne "+str(zsakmany)+" arannyal.")
                print("")
            else:
                m = monsters[randint(0,len(monsters)-1)]
                new_m = Monster(m.name,m.max_hp,m.hp,m.min_dmg,m.max_dmg,m.xp,m.gold)
                battle(p,new_m)

def battle (p,m):
    print("")
    print("Randa "+m.name+" támad rád, akinek "+str(m.max_hp)+ " élete van.")
    harci_dontes = str(input("Megtámadod (1), vagy elfutsz mint a nyúl (2)?"))
    while harci_dontes not in ("1","2"):
        print("Mondom 1 vagy 2!")
        harci_dontes = str(input("Megtámadod (1), vagy elfutsz mint a nyúl (2)?"))
        continue
    if harci_dontes == "2":
        veszteseg = min(p.gold,randint(1,3))
        p.gold = max(p.gold - veszteseg,0)
        print("")
        print("Bátorságod akár a nyúlé...")
        print("Megmenekültél, de "+str(veszteseg)+" aranyad a "+m.name+" mancsában maradt.")
    else:
        while m.hp > 0 and p.hp > 0:
            sajat_sebzes = randint(p.min_dmg,p.max_dmg)+p.bonus_dmg
            szorny_sebzes = randint(m.min_dmg,m.max_dmg)
            m.hp -= sajat_sebzes
            p.hp -= szorny_sebzes
            print("")
            print("Megcsaptad a dögöt. -"+str(sajat_sebzes)+"hp")
            print("De ő is megkarmolt téged -"+str(szorny_sebzes)+"hp")
            if p.hp <= 0:
                print("")
                print("Agyoncsapott a szörny.")
                print("Meghaltál, vége a játéknak.")
                print("Játszunk legközelebb is!")
                break
            elif m.hp <= 0:
                print("")
                print("Elpusztítottad a rusnya lényt. Ügyes vagy!")
                p.xp += m.xp
                p.gold += m.gold
                if p.xp >= p.xp_max:
                    level_up(p)
                break
            else:
                print(str(p.hp)+"/"+str(p.max_hp)+" életed van.")
                print("A szörnynek "+str(m.hp)+"/"+str(m.max_hp)+" élete maradt.")
                print("")
                continue

def level_up (p):
    hp_change = int(p.max_hp * 0.3)
    xp_change = int(p.xp_max * 0.5)
    dmg_change = int(p.level * 0.5) + 1
    p.level += 1
    p.max_hp += hp_change
    p.hp = p.max_hp
    p.xp = 0
    p.xp_max += xp_change
    p.bonus_dmg += dmg_change
    print("")
    print("Elég tapasztalatot gyűjtöttél ahhoz hogy szintet lépj.")
    print("!!!" + str(p.level) + ". szintre lépsz!!!")
    print("+" + str(hp_change) + " hp")
    print("+" + str(xp_change) + " max xp")
    print("+" + str(dmg_change) + " sebzés")


a = menu()
if a == "1":
    monster_add()
    name = input("Add meg a neved!")
    print("Üdvözöllek Sir "+name+"!")
    generate_map(10,10)
    init_hp = 20 + randint(-5,5)
    player = Player(name,init_hp,init_hp,0,2,4,0,10,0,1,0)
    roads(player)
          
                
                                    
