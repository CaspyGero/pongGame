def gamePong(width, height, speed):
    import pygame
    from os import path
    #Initial variables
    global isOnline, hostOrClient
    global host, client
    pygame.init()
    pygame.display.set_caption("Pong")
    logoPong = pygame.image.load(path.dirname(__file__) + "/logoPong.png")
    pygame.display.set_icon(logoPong)
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True
    start = False
    #Define variables
    margin = {"up" : 30, "right" : 20, "down" : 20, "left" : 20}
    directionPlayer1 = speed
    directionPlayer2 = -speed
    directionBall = pygame.Vector2(speed * (3/5), speed * (3/5))
    positionBall = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    points = {"player1" : 0, "player2" : 0}
    font = pygame.font.Font(None, 50)
    pointsText = font.render((str(points["player1"]) + " - " + str(points["player2"])), 1, "white")
    startText = font.render("Press space to start", 1, "white")
    centerPoints = pointsText.get_rect()
    centerPoints.centerx = screen.get_width() // 2
    centerPoints.centery = 15
    centerStart = startText.get_rect()
    centerStart.centerx = screen.get_width() // 2
    centerStart.centery = screen.get_height() // 2 - 30
    #Online function
    if isOnline == "s":
        import socket
        playerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        playerSocket.settimeout(0.5)
        if hostOrClient == "host":
            playerSocket.bind(host)
        else:
            playerSocket.bind(client) 
    #Principal function
    while running:
        #Reset variables
        positionPlayer1 = pygame.Vector2(margin["left"] + 25, screen.get_height() / 2)
        positionPlayer2 = pygame.Vector2(screen.get_width() - margin["right"] - 16 - 25, screen.get_height() / 2)
        positionBall = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        #Detect actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                            
        #Draw sprites
        screen.fill("black")
        pointsText = font.render((str(points["player1"]) + " - " + str(points["player2"])), 1, "white")
        screen.blit(pointsText, centerPoints)
        screen.blit(startText, centerStart)
        pygame.draw.line(screen, "white", (margin["left"], margin["up"]), (screen.get_width() - margin["right"], margin["up"]), 2)
        pygame.draw.line(screen, "white", (screen.get_width() - margin["right"], margin["up"]), (screen.get_width() - margin["right"], screen.get_height() - margin["down"]), 2)
        pygame.draw.line(screen, "white", (screen.get_width() - margin["right"], screen.get_height() - margin["down"]), (margin["left"], screen.get_height() - margin["down"]), 2)
        pygame.draw.line(screen, "white", (margin["left"], screen.get_height() - margin["down"]), (margin["left"], margin["up"]), 2)
        player1 = pygame.draw.rect(screen, "white", (positionPlayer1.x, positionPlayer1.y, 16, 64))
        player2 = pygame.draw.rect(screen, "white", (positionPlayer2.x, positionPlayer2.y, 16, 64))
        ball = pygame.draw.circle(screen, "white", positionBall, 10)
        #Update screen
        pygame.display.flip()
        clock.tick(60)
        #Check if the other started
        if isOnline == "s":
            if start == False:
                #Try por si no llegan datos
                try:
                    data, host = playerSocket.recvfrom(1024)
                except socket.timeout:
                    data = "None"
                    pass
                if(data.decode() == "True"):
                    start = True
            else:
                playerSocket.sendto(b"True", client if hostOrClient == "host" else host)
        #Only start when space was pressed
        while start:
            #Detect actions
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                    running = False
                    continue
                if event.type == pygame.KEYDOWN:
                    #Player 1
                    if event.key == pygame.K_w:
                        directionPlayer1 = -speed
                    if event.key == pygame.K_s:
                        directionPlayer1 = speed
                    #Player 2
                    if event.key == pygame.K_UP:
                        directionPlayer2 = -speed
                    if event.key == pygame.K_DOWN:
                        directionPlayer2 = speed
            #Mobile objects coordinates
            positionBall.x += directionBall.x
            positionBall.y += directionBall.y
            if positionBall.y < margin["up"] + 10 or positionBall.y > screen.get_height() - margin["down"] - 10:
                directionBall.y *= -1
            positionPlayer1.y += directionPlayer1
            positionPlayer2.y += directionPlayer2
            if positionPlayer1.y < margin["up"]:
                positionPlayer1.y = margin["up"]
            elif positionPlayer1.y > screen.get_height() - margin["down"] - 64:
                positionPlayer1.y = screen.get_height() - margin["down"] - 64
            if positionPlayer2.y < margin["up"]:
                positionPlayer2.y = margin["up"]
            elif positionPlayer2.y > screen.get_height() - margin["down"] - 64:
                positionPlayer2.y = screen.get_height() - margin["down"] - 64
            #Define if someone wins points
            if positionBall.x < margin["left"] + 10:
                points["player2"] += 1
                start = False
            elif positionBall.x > screen.get_width() - margin["right"] - 10:
                points["player1"] += 1
                start = False
            #Draw sprites
            screen.fill("black")
            pointsText = font.render((str(points["player1"]) + " - " + str(points["player2"])), 1, "white")
            screen.blit(pointsText, centerPoints)
            pygame.draw.line(screen, "white", (margin["left"], margin["up"]), (screen.get_width() - margin["right"], margin["up"]), 2)
            pygame.draw.line(screen, "white", (screen.get_width() - margin["right"], margin["up"]), (screen.get_width() - margin["right"], screen.get_height() - margin["down"]), 2)
            pygame.draw.line(screen, "white", (screen.get_width() - margin["right"], screen.get_height() - margin["down"]), (margin["left"], screen.get_height() - margin["down"]), 2)
            pygame.draw.line(screen, "white", (margin["left"], screen.get_height() - margin["down"]), (margin["left"], margin["up"]), 2)
            player1 = pygame.draw.rect(screen, "white", (positionPlayer1.x, positionPlayer1.y, 16, 64))
            player2 = pygame.draw.rect(screen, "white", (positionPlayer2.x, positionPlayer2.y, 16, 64))
            ball = pygame.draw.circle(screen, "white", positionBall, 10)
            #Collitions
            if ball.colliderect(player1) or ball.colliderect(player2):
                directionBall.x *= -1
            #Update screen
            pygame.display.flip()
            clock.tick(60)
            #Send and recieve variables
            if isOnline == "s":
                if hostOrClient == "host":
                    string = f"playerPosition={positionPlayer1.y}, playerDirection={directionPlayer1}"
                    playerSocket.sendto(string.encode(), client)
                    #Try por si no llegan datos
                    try:
                        data, host = playerSocket.recvfrom(1024)
                    except socket.timeout:
                        pass
                else:
                    #Try por si no llegan datos
                    try:
                        data, host = playerSocket.recvfrom(1024)
                    except socket.timeout:
                        pass
                    string = f"playerPosition={positionPlayer2.y}, playerDirection={directionPlayer2}"
                    playerSocket.sendto(string.encode(), host)
                data = data.decode().split(", ")
                if len(data) == 2:
                    if data[0].startswith("playerPosition="):
                        if hostOrClient == "host":
                            positionPlayer2.y = int(data[0].split("=")[1])
                        else:
                            positionPlayer1.y = int(data[0].split("=")[1])
                    if data[1].startswith("playerDirection="):
                        if hostOrClient == "host":
                            directionPlayer2 = int(data[1].split("=")[1])
                        else:
                            directionPlayer1 = int(data[1].split("=")[1])
                
    pygame.quit()
    if __name__ == "__main__":
        if isOnline == None or isOnline == "n":
            launcher()
        else:
            playerSocket.close()

def startGame():
    global root
    global isOnline
    width = int(inputWidth.get())
    height = int(inputHeight.get())
    speed = int(inputSpeed.get())
    root.destroy()
    if isOnline == None or isOnline == "n":
        gamePong(width, height, speed)
    else:
       online.host(width, height, speed) 

def resetValues():
    global inputWidth, inputHeight, inputSpeed
    inputWidth.delete(0, "end")
    inputHeight.delete(0, "end")
    inputSpeed.delete(0, "end")
    inputWidth.insert(0, 768)
    inputHeight.insert(0, 512)
    inputSpeed.insert(0, 5)

def launcher():
    global inputWidth, inputHeight, inputSpeed, root
    import tkinter
    from os import path
    root = tkinter.Tk()
    root.title("Pong launcher")
    root.geometry("300x175+600+300")
    root.resizable(0,0)

    frameMain = tkinter.Frame(root, width=130)
    frameMain.pack(side=tkinter.RIGHT, fill=tkinter.Y, padx=20, pady=5)
    frameImage = tkinter.Frame(root, width=140)
    frameImage.pack(side=tkinter.LEFT, fill=tkinter.Y, padx=5, pady=5)
    
    imageFile = path.dirname(__file__) + "/imagenPong.png"
    image = tkinter.PhotoImage(file=imageFile)

    labelImage = tkinter.Label(frameImage, image=image)
    labelImage.pack()

    labelWidth = tkinter.Label(frameMain, text="Enter the width: ", justify="center")
    labelWidth.pack()
    inputWidth = tkinter.Entry(frameMain)
    inputWidth.pack()
    inputWidth.insert(0, 768)

    labelHeight = tkinter.Label(frameMain, text="Enter the height: ", justify="center")
    labelHeight.pack()
    inputHeight = tkinter.Entry(frameMain)
    inputHeight.pack()
    inputHeight.insert(0, 512)

    labelSpeed = tkinter.Label(frameMain, text="Enter the speed: ", justify="center")
    labelSpeed.pack()
    inputSpeed = tkinter.Entry(frameMain)
    inputSpeed.pack()
    inputSpeed.insert(0, 5)

    buttonStart = tkinter.Button(frameMain, text="Reset values", command=resetValues)
    buttonStart.pack(pady=10, side=tkinter.LEFT)
    buttonStart = tkinter.Button(frameMain, text="Start game", command=startGame)
    buttonStart.pack(pady=10, side=tkinter.RIGHT)

    root.mainloop()

class online:
    def host(width, height, speed):
        global client, host
        import socket
        hostIP = socket.gethostbyname(socket.gethostname()) 
        hostPort = 50574
        host = hostIP, hostPort
        hostSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        hostSocket.bind(host)
        print("UDP host up and listening")
        print(f"Host ip is: {hostIP}\nHost port is: {hostPort}")
        hostWaiting = True
        while hostWaiting:
            data, client = hostSocket.recvfrom(1024)
            if data.decode() == "Connected!":
                print("Connected by:", client)
                hostSocket.sendto(b"Connection confirmation", client)
                hostWaiting = False
        hostSocket.sendto(f"width={width}, height={height}, speed={speed}".encode(), client)
        hostSocket.close()
        gamePong(width, height, speed)
    def client():
        import socket
        from time import sleep
        global host, client
        clientIP = socket.gethostbyname(socket.gethostname()) 
        clientPort = 50574 #Standar port
        client = clientIP, clientPort
        print(f"client ip is: {clientIP}\nclient port is: {clientPort}")
        print()
        hostIP = input("Enter the host's ip: ")
        hostPort = 50574 #Standar port
        host = hostIP, hostPort
        clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        clientSocket.bind(client)
        clientWaiting = True
        #RECIBIR DATOS DE CONFIRMACION
        while clientWaiting:
            clientSocket.sendto(b"Connected!", host)
            data, host = clientSocket.recvfrom(1024)
            if data.decode() == "Connection confirmation":
                width, height, speed = None, None, None
                while width == None or height == None or speed == None:
                    data, host = clientSocket.recvfrom(1024)
                    data = data.decode().split(", ")
                    if len(data) == 3:
                        if data[0].startswith("width="):
                            width = int(data[0].split("=")[1])
                        if data[1].startswith("height="):
                            height = int(data[1].split("=")[1])
                        if data[2].startswith("speed="):
                            speed = int(data[2].split("=")[1])
            else:
                sleep(1)
                continue
            clientWaiting = False
        clientSocket.close()
        gamePong(width, height, speed)

while __name__ == "__main__":
    isOnline = input("Online (S/n)? ").lower()
    if isOnline == "s":
        hostOrClient = input("Host or client? ").lower()
        if hostOrClient == "host":
            launcher()
        elif hostOrClient == "client":
            online.client()
    elif isOnline == "n":
        launcher()