#(speedVar,bar_len,ball_rad,ball_speed)
#(10,120,25,5)
class Stack:
    def __init__(self):
         self.list = [ (1.3,120,20,6) ,(1.25,120,20,5.9),(1.2,120,20,5.7),(1.1,125,25,5.3),(1.1,130,25,5)]
    def pop(self):
        return self.list.pop()
    def isEmpty(self):
         return True if len(self.list) == 0 else False

