
class roomtype:
    class library:
        guic='red'
        def describe()->str:
            return  'knowlage flows from the walls, the library expands around you. '
        def getitems():
            return  {2:'books     \033[0m(boring as fuck)', 5:'explosives    \033[0m(alah hulacba)'}
        def getenimies():
            return ['jeff the goblin']
        def __str__()->str:
            return 'regular'

    class regular:
        guic='gray'
        def describe()->str:
            return  'stupid room'
        def getitems():
            return  {2:'cokeaddicts', 5:'explosives'}
        def getenimies():
            return ['jeff the goblin']
        def __str__()->str:
            return 'regular'
"""   items and actual monsters should be added in, then advanced d gen should str the objects to print them.  """
