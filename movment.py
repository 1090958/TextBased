import random

class d2:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __str__(self)->str:
        return f'{self.x}, {self.y}'

class dungeon:

    class room:
        def __init__(self, location:tuple) -> None:
            self.doors=[]
            self.connectrooms=[]
            self.coords=d2(location[0], location[1])
        def moveops(self)->dict:
            '''returns all movment options from self.to other rooms.'''
            t=lambda x: ['north','south'] if self.coords.y!=x.coords.y else ['east','west']
            m=lambda x: t(x)[0] if  x.coords.y>self.coords.y or x.coords.x>self.coords.x else t(x)[1]

            i={i:m(i) for i in self.connectrooms}

            return i
                
                
        def __str__(self) -> str:
            return f'room({self.coords.x, self.coords.y})'
        
    class door:
        def __init__(self, r1, r2) -> None:
            self.r1,self.r2=r1,r2
            if type(self.r1)!= dungeon.room:
                raise TypeError(f'{str(self.r1)} is {type(self.r1)}, {str(self.r1)} must be a room')
            if type(self.r2)!=dungeon.room:
                raise TypeError(f'{str(self.r2)} is {type(self.r2)}, {str(self.r2)} must be a room')
            self.r1.connectrooms.append(self.r2)
            self.r2.connectrooms.append(self.r1)
            self.r1.doors.append(self)
            self.r2.doors.append(self)
        

        def delete(self) -> None:
            self.r1.connectrooms.remove(self.r2)
            self.r2.connectrooms.remove(self.r1)
            self.r1.doors.remove(self)
            self.r2.doors.remove(self)
            

        def __str__(self) -> str:
            return f'door({self.r1}, {self.r2})'
        
    class new_dungeon:    
        def __init__(self, size:tuple,
                     rds=100) -> None:

            self.size=d2(size[0], size[1])
            self.rooms=[ [dungeon.room((x, y)) for y in range(self.size.x)] for x in range(self.size.y)]
            self.doors=[]
            for k in self.rooms:
                for i in k:
                    for l in self.rooms:
                        for j in l:
                            if (i.coords.x==j.coords.x and i.coords.y+1==j.coords.y) or (i.coords.y==j.coords.y and i.coords.x+1==j.coords.x):  self.doors.append(dungeon.door(i,j))

            for i in self.doors:
                if random.random() < rds:
                    i.delete()
                    self.doors.pop(self.doors.index(i))
                    

if __name__=='__main__':
    a=dungeon.new_dungeon((30, 30), 0.25)


    rm=a.rooms[7][3]
    while True:
        print('you enter a dimlit room')
        print(f'your coordinates are ({rm.coords})')

        print('you see ')
        [print(f'a door heading {i[1]} to ({str(i[0].coords)})') for i in rm.moveops().items()]


        a=input('move?')

        unexpectedinput=True

        for i in rm.moveops().items():
            if a==i[1]:
                rm=i[0]
                unexpectedinput=False
        if unexpectedinput: 
            print('that is not an option')




