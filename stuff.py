import random,settings

class Effect:
    def __init__(self, name:str, effect:str, level:int, time:int) -> None:
        self.name = name
        self.effect = effect
        self.level = level
        self.time = time
    def copy(self):
        return Effect(self.name, self.effect, self.level, self.time)

fire = Effect("Fire","health",-10,9)
con1 = Effect("Health Boost I","constitution",10,12)
dex1 = Effect("Heightened Reflexes I","dexterity",10,12)
dex10 = Effect("Heightened Reflexes X","dexterity",1000,12)
str10 = Effect("Strong Boi X","strength",1000,12)





class Enchantment:
    def __init__(self, name:str, effect:str, level:int) -> None:
        self.name = name
        self.effect = effect
        self.level = level

steal = Enchantment("Curse of Stealing I","steal",40)
flame = Enchantment("Flame I",fire,1)
prot1 = Enchantment("Protection I","protect",6)
prot2 = Enchantment("Protection II","protect",10)





class Rarity:
    def __init__(self, name:str, colour:tuple) -> None:
        self.name = name
        self.colour = colour
    def __str__(self) -> str:
        return self.name

common = Rarity("common",(110,110,110))
uncommon = Rarity("uncommon",(0,110,0))
rare = Rarity("rare",(0,50,220))
epic = Rarity("epic",(100,0,220))
legendary = Rarity("legendary",(220,100,0))
mythic = Rarity("mythic",(150,150,0))





class ObjectType:
    def __init__(self, name:str, image:str, rarity:Rarity, use:str, value:int|float, data:dict) -> None:
        self.name = name
        self.img = image
        self.rarity = rarity
        self.use = use
        self.value = value
        self.data = data

class Object:
    def __init__(self, _type:ObjectType) -> None:
        self.type = _type
        if "uses" in self.type.data:
            self.uses = self.type.data["uses"]
    

basicHelmet = ObjectType("Basic Helmet", "test.jpg", uncommon, "armour0", 30, {"protection":5,"enchantments":[],"effects":[]})
enchIronLeggings = ObjectType("Enchanted Iron Chestplate", "test.jpg", rare, "armour2", 140, {"protection":7,"enchantments":[prot1],"effects":[]})
coolChestplate = ObjectType("Cool Chestplate", "test.jpg", legendary, "armour1", 140, {"protection":20,"enchantments":[prot2],"effects":[]})
cocaine = ObjectType("Cocaine", "test.jpg", epic, "effect", 75, {"uses":5,"enchantments":[],"effects":[dex10]})
randomPills = ObjectType("Random Pills", "test.jpg", rare, "effect", 50, {"uses":3,"enchantments":[],"effects":[str10]})
basicSword = ObjectType("Basic Sword", "test.jpg", common, "weapon", 20, {"attack":25,"stamina":25,"hitRate":90,"enchantments":[],"effects":[]})
goodSword = ObjectType("Lifesteal Sword", "test.jpg", epic, "weapon", 95, {"attack":10,"stamina":25,"hitRate":90,"enchantments":[steal],"effects":[]})





class CharacterType:
    def __init__(self, name:str, data:dict) -> None:
        self.name = name
        self.data = data
    def __str__(self) -> str:
        return f"CharacterType({self.name}, {self.data})"

class Character:
    def __init__(self, _type:CharacterType, name:str|None=None) -> None:
        self.type = _type
        if name==None: self.name=self.type.name
        else: self.name=name
        self.inv = []
        if "inventory" in self.type.data:
            for i in range(self.type.data["invSize"]):
                if random.random()<self.type.data["invChance"]: self.inv.append(Object(self.type.data["inventory"][i]))
        self.hp = self.type.data["health"]
        self.stamina = 0
        self.armour = [None,None,None,None]
        self.effects = []
        self.skills = {"constitution":110,"dexterity":125,"strength":115}

player = CharacterType("Player", {"health":200,"attack":20,"defense":15,"staminaRate":20})
npc = CharacterType("Default NPC", {"health":150,"attack":10,"defense":10,"staminaRate":10})
goblin1 = CharacterType("Small Goblin", {"health":30,"attack":7,"defense":10,"staminaRate":10})
goblin2 = CharacterType("Fast Goblin", {"health":50,"attack":5,"defense":25,"staminaRate":20})
goblin3 = CharacterType("Angry Goblin", {"health":50,"attack":20,"defense":10,"staminaRate":20,"invSize":1,"inventory":[basicSword],"invChance":0.4})
goblin4 = CharacterType("Big Goblin", {"health":100,"attack":35,"defense":20,"staminaRate":25,"invSize":1,"inventory":[basicSword],"invChance":0.7})





class Encounter:
    def __init__(self, team1:list[Character], team2:list[Character]) -> None:
        self.playerTeam = team1
        for char in self.playerTeam:
            char.team = 1
        self.enemyTeam = team2
        for char in self.enemyTeam:
            char.team = 2
        self.people = team1+team2
        random.shuffle(self.people)
        self.playerSelected = 0
        self.time = -1
        self.winner = None
    def update(self, _input:list[str]) -> str:
        output = ""
        validInput = True
        if not _input:
            pass
        elif _input[0]=="use":
            if -3<int(_input[1])<5: self.playerSelected = int(_input[1])
            else: validInput = False
        elif _input[0] in ["wait","skip"]:
            self.playerSelected = -2
        else:
            validInput = False
        if not validInput:
            output += (f"Invalid Input, automatically using slot {self.playerSelected} \n")
        if self.time==-1:
            output += ("You get caught in a fight! \n")
            output += ("Enemies: \n")
            for enemy in self.enemyTeam:
                output += (f"  - {enemy.name} ({enemy.type.name}) \n")
                enemy.stamina = 0
            output += ("Your Team: \n")
            for char in self.playerTeam:
                output += (f"  - {char.name} ({char.type.name}) \n")
                char.stamina = 0
            output += ("Enter to continue \n")
            self.time += 1
        else:
            while True:
                self.time += 1
                for char in self.people:
                    if char.type.name=="Player": slot = self.playerSelected
                    elif char.inv==[]: slot = -1
                    else: slot = random.randint(0,len(char.inv)-1)
                    char.hp += sum([e.level for e in char.effects if e.effect=="health"])
                    maxHp = int(char.type.data["health"]*(char.skills["constitution"]/100)*(sum([100]+[e.level for e in char.effects if e.effect=="constitution"])/100))
                    if char.hp>maxHp: char.hp = maxHp
                    for eff in char.effects[:]:
                        eff.time -= 1
                        if eff.time <= 0:
                            char.effects.remove(eff)
                    if (slot==-1 or char.inv[slot]==None) and slot!=-2:
                        if char.stamina>char.type.data["staminaRate"]*3:
                            for enemy in self.people:
                                if char.team != enemy.team:
                                    if random.random()<(enemy.skills["dexterity"]/100)*(sum([100]+[e.level for e in enemy.effects if e.effect=="dexterity"])/100)*(enemy.type.data["defense"]/100):
                                        output += (f"{char.name} tries to attack but {enemy.name} dodges! \n")
                                    else:
                                        damage = char.type.data["attack"]
                                        prot = sum(sum(e.level for e in a.type.data["enchantments"] if e.effect=="protect")+a.type.data["protection"] for a in enemy.armour if a)
                                        if prot>40: prot=40
                                        damage -= int((prot/100)*damage)
                                        output += (f"{char.name} attacks {enemy.name}! (-{damage}HP) \n")
                                        enemy.hp -= damage
                                        char.stamina -= char.type.data["staminaRate"]*3
                    elif slot!=-2 and ("stamina" not in char.inv[slot].type.data or char.stamina>char.inv[slot].type.data["stamina"]):
                        if char.inv[slot].type.use=="weapon":
                            for enemy in self.people:
                                if char.team != enemy.team:
                                    if random.random()<char.inv[slot].type.data["hitRate"]/100:
                                        if random.random()<(enemy.skills["dexterity"]/100)*(sum([100]+[e.level for e in enemy.effects if e.effect=="dexterity"])/100)*(enemy.type.data["defense"]/100):
                                            output += (f"{char.name} tries to attack but {enemy.name} dodges! \n")
                                        else:
                                            damage = char.inv[slot].type.data["attack"]
                                            prot = sum(sum(e.level for e in a.type.data["enchantments"] if e.effect=="protect")+a.type.data["protection"] for a in enemy.armour if a)
                                            if prot>40: prot=40
                                            output += (f"{char.name} attacks {enemy.name} with a {char.inv[slot].strShort()}! (-{damage}HP) \n")
                                            if not random.random()<(char.inv[slot].type.data["hitRate"]/100):
                                                new = int(damage*(char.skills["strength"]/100)*sum([100]+[e.level for e in char.effects if e.effect=="strength"])/100)
                                                output += (f"{char.name} got a double hit! (-{new-damage}HP) \n")
                                                damage += new
                                            if any([ench.effect=="steal" for ench in char.inv[slot].type.data["enchantments"]]):
                                                x = [ench for ench in char.inv[slot].type.data["enchantments"] if ench.effect=="steal"]
                                                output += (f"{char.name} uses {x[0]} to steal health!")
                                                char.hp += int((x[0].level/100)*damage)
                                            enemy.hp -= damage
                                            char.stamina -= char.inv[slot].type.data["stamina"]
                                            for ench in char.inv[slot].type.data["enchantments"]:
                                                if isinstance(ench.effect, Effect):
                                                    enemy.effects.append(ench.effect)
                                            if "uses" in char.inv[slot].type.data:
                                                char.inv[slot].uses -= 1
                                    else:
                                        output += (f"{char.name} tries to attack {enemy.name} but misses! \n")
                        elif char.inv[slot].type.use=="instant":
                            output += (f"{char.name} uses {char.inv[slot].type.strShort()} \n")
                            if "healing" in char.inv[slot].type.data:
                                char.hp += char.inv[slot].type.data["healing"]
                                maxHp = int(char.type.data["health"]*(char.skills["constitution"]/100)*(sum([100]+[e.level for e in char.effects if e.effect=="constitution"])/100))
                                if char.hp>maxHp: char.hp = maxHp
                            if "stamina" in item.type.data:
                                char.stamina += item.type.data["stamina"]
                            char.inv[slot].uses -= 1
                        elif char.inv[slot].type.use=="effect":
                            output += (f"{char.name} uses {char.inv[slot].type.strShort()} \n")
                            for eff in char.inv[slot].type.data["effects"]:
                                char.effects.append(eff.copy())
                            char.inv[slot].uses -= 1
                    char.stamina += char.type.data["staminaRate"]
                    for eff in char.effects[:]:
                            if any([e!=eff and e.effect==eff.effect and e.time>=eff.time for e in char.effects]): char.effects.remove(eff)
                    for item in char.inv:
                        if item and "uses" in item.type.data and item.uses<1:
                            char.inv[char.inv.index(item)] = None
                leave = False
                for char in self.people:
                    if char.hp <= 0:
                        output += (f"{char.name} has fallen! \n")
                        if char.type.name=="Player":
                            output += ("You lost the battle! \n")
                            self.winner = 2
                            leave = True
                        self.people.remove(char)
                if sum([1 for c in self.people if c.team==2])==0 and not self.winner:
                    output += ("You have won the battle! \n")
                    self.winner = 1
                    leave = True
                p = next(iter([c for c in self.people if c.type.name=="Player"]),None)
                if p and any([p.stamina>item.type.data["stamina"] for item in p.inv if (item!=None and item.type.use=="weapon")]):
                    leave = True
                if leave:
                    if not self.winner:
                        output += ("Your Turn \n")
                        for item in [i for i in p.inv if i!=None]:
                            if item.type.use=="weapon": output += (f"{p.inv.index(item)}: {item.uses if 'uses' in item.type.data else 1}x {item.strShort()}"+(" "*(30-len(item.type.name)))+f"{p.stamina}/"+str(item.type.data["stamina"])+"\n")
                            elif item.type.use in ["instant","effect"]: output += (f"{p.inv.index(item)}: {item.uses if 'uses' in item.type.data else 1}x {item.strShort()}"+(" "*(30-len(item.type.name)))+"No Stamina Needed \n")
                        if p.effects != []:
                            output += ("Effects: \n")
                            for eff in p.effects:
                                output += (f"{eff} \n")
                    break
        return output
    def endUpdate(self) -> tuple[str|Character|list]:
        for char in self.people:
            if char.type.name=="Player":
                x = char
                self.people.remove(char)
        return x, self.people





class Room:
    def __init__(self, place:tuple[int], biome:int, _type:int, connections:tuple[int]) -> None:
        self.place = place
        self.biome = biome
        self.type = _type
        self.connections = connections
        self.seen = False
        self.contents = []
        self.characters = []
        self.shopStuff = []
    def copy(self):
        return Room(self.place, self.biome, self.type, self.connections)
    def __str__(self) -> str:
        return f"Room({self.place},{self.biome},{self.type},{self.connections})"

class Map:
    def __init__(self, size:int, spawn:tuple[int]) -> None:
        self.size = size
        self.spawn = spawn
        self.rooms = [[None for x in range(size)] for y in range(size)]
    def update(self, loc:tuple[int], info:tuple[int]):
        self.rooms[loc[0]][loc[1]] = Room(loc,info[0],info[1],info[2])
    def print(self) -> str:
        for i in self.rooms:
            for j in i:
                print(j)

# ["Normal","Fire","Water","Mines"]
# ["Normal Room","Dungon","Dungon","Dungon","Blacksmith","General Shop","Dodgy Shop","Boss Fight"]

def generateMap(x:str) -> Map:
    stuff,seed = x.split()
    size,biomes,types,sx,sy = [int(i) for i in stuff.split(".")]
    output = Map(size,(sx,sy))
    for i in range(size**2):
        n = ord(seed[i])
        if n>126: n-=68
        else: n-=34
        if n>-1:
            con = [int(j) for j in bin(n//(biomes*types))[2:]]
            if len(con)<4: con = tuple([0]*(4-len(con))+con)
            else: con = tuple(con)
            room = updateRoom(Room((i//size,i%size),(n//types%biomes),(n%types),con))
            output.rooms[i//size][i%size] = room
    return output

def updateRoom(room:Room) -> Room:
    if room.type==1:
        characters = random.choice([[goblin1,goblin2,goblin3,goblin4]])
        room.characters = [Character(i) for i in random.choices(characters, weights=(4,0,0,0), k=random.randint(3,5))]
    elif room.type==2:
        characters = random.choice([[goblin1,goblin2,goblin3,goblin4]])
        room.characters = [Character(i) for i in random.choices(characters, weights=(2,4,3,1), k=random.randint(4,7))]
    elif room.type==3:
        characters = random.choice([[goblin1,goblin2,goblin3,goblin4]])
        room.characters = [Character(i) for i in random.choices(characters, weights=(1,3,4,2), k=random.randint(5,8))]
    elif room.type==4:
        objects = [basicSword,basicHelmet,cocaine,randomPills,coolChestplate]
        room.shopStuff = [i for i in random.choices(objects, k=random.randint(4,5))]
        room.shopStuff = list(dict.fromkeys(room.shopStuff))
    elif room.type==5:
        objects = [basicSword,basicHelmet,cocaine,randomPills,coolChestplate]
        room.shopStuff = [i for i in random.choices(objects, k=random.randint(3,6))]
        room.shopStuff = list(dict.fromkeys(room.shopStuff))
    elif room.type==6:
        objects = [basicSword,basicHelmet,cocaine,randomPills,coolChestplate]
        room.shopStuff = [i for i in random.choices(objects, k=random.randint(3,4))]
        room.shopStuff = list(dict.fromkeys(room.shopStuff))
    return room