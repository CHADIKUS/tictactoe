from operator import index
from os import stat
from tabnanny import check
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="%", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="%how"))
    print("BOT IS ON")


board = [["b","b","b"],["b","b","b"],["b","b","b"]]
ongoing = False
plr1 = ""
plr2 = ""

turn = "x"

@bot.event
async def on_message(message):
    global ongoing
    global plr1
    global plr2
    global turn
    global board
    if message.content == "%how".lower():
        await message.channel.send("%start = starts match \n %join = join a match \n %play [x coordinate] [y coordinate]")
    if message.content == "%start":
        end_message = ""
        if ongoing == True:
            end_message = "ongoing match, please wait"
        else:
            ongoing = True
            plr1 = message.author.id
            end_message = "match started, other player must send %join"
        await message.channel.send(end_message)
    if message.content == "%join":
        end_message = ""
        if plr2 == "":
            if plr1 == "":
                end_message = "no match started, do %start to make one"
            else:
                if message.author.id == plr1:
                    end_message = "you cant join your own game"
                else:
                    plr2 = message.author.id
                    end_message = "**" + message.author.name + "**" + " has joined the game"
        else:
            end_message = "ongoing match, please wait"
        await message.channel.send(end_message)
        await message.channel.send(render_board())


    if "%play" in message.content:
        end_message = ""

        if message.author.id != 1028407029339009054:


            if ongoing == True:
                if message.author.id == plr1 or message.author.id == plr2:
                    team = ""
                    if message.author.id == plr1:
                        team = "x"
                    else:
                        team = "o"
                    split_msg = message.content.split()
                    
                    if team == turn:
                        if move(team,int(split_msg[1]),int(split_msg[2])) == "clear":
                            if team == "x":
                                turn = "o"
                            else:
                                turn = "x"

                            end_message = render_board()
                            
                            if check_win() == "o_win":
                                end_message += "\n***O WINS***"
                                ongoing = False
                                turn = "x"
                                plr1 = ""
                                plr2 = ""
                                board = [["b","b","b"],["b","b","b"],["b","b","b"]]
                            elif check_win() == "x_win":
                                end_message += "\n***X WINS***"
                                ongoing = False
                                turn = "x"
                                plr1 = ""
                                plr2 = ""
                                board = [["b","b","b"],["b","b","b"],["b","b","b"]]
                            elif check_win() == "tie":
                                end_message += "\n***TIE***"
                                ongoing = False
                                turn = "x"
                                plr1 = ""
                                plr2 = ""
                                board = [["b","b","b"],["b","b","b"],["b","b","b"]]


                        elif move(team,int(split_msg[1]),int(split_msg[2])) == "taken":
                            end_message = "this spot is already taken"
                        elif move(team,int(split_msg[1]),int(split_msg[2])) == "impossible":
                            end_message = "that spot isn't possible \n only spots 1-3 work"
                    
                    
                    else:
                        end_message = "not your turn"
                else:
                    end_message = "not your game"
            else:
                end_message = "no match started, do %start to make one"

            await message.channel.send(end_message)

def move(team, x , y):

    status = ""

    if x < 1 or x > 3 or y < 1 or y > 3:
        status = "impossible"
    else:
        if board[y-1][x-1] == "b":
            board[y-1][x-1] = team
            status = "clear"
        else:
            status = "taken"

    return(status)


def check_win():
    #checks alignment horizontally 
    for y in board:
        total = ""
        for x in y:
            total += x
        if total == "xxx":
            return("x_win")
        elif total == "ooo":
            return("o_win")

    #checks alignment vertically
    for i in range(3):
        total = ""
        for y in board:
            total += y[i-1]
        if total == "xxx":
            return("x_win")
        elif total == "ooo":
            return("o_win")

    #checks diagonal to right
    if board[1][1] != "b":
        total = ""
        total += board[0][0]
        total += board[1][1]
        total += board[2][2]
        if total == "xxx":
            return("x_win")
        elif total == "ooo":
            return("o_win")

    #checks diagonal to left
    if board[1][1] != "b":
        total = ""
        total += board[2][0]
        total += board[1][1]
        total += board[0][2]
        if total == "xxx":
            return("x_win")
        elif total == "ooo":
            return("o_win")
        
    #checks if all spots are taken
    if board[2][2] != "b":
        total = ""
        for y in board:
            for x in y:
                total += x
        
        if "b" in total:
            pass
        else:
            return("tie") 

    return("continue")

def render_board():
    rendered_board = ""
    for i in board:
        for o in i:
            tile = ""
            if o == "b":
                tile = ":black_large_square: "
            elif o == "x":
                tile = ":x: "
            elif o == "o":
                tile = ":o: "
            rendered_board += tile

        rendered_board += "\n"   
    return rendered_board
    

bot.run("TOKEN HERE")