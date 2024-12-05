def gamePong(width, height, speed):
    import pygame
    from os import path
    global start, running, points, positionPlayer1, directionPlayer1, positionPlayer2, directionPlayer2, positionBall, directionBall
    pygame.init()
    pygame.display.set_caption("Pong")
    logoPong = pygame.image.load(path.dirname(__file__) + "/logoPong.png")
    pygame.display.set_icon(logoPong)
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    #Define variables
    margin = {"up" : 30, "right" : 20, "down" : 20, "left" : 20}
    directionPlayer1 = speed
    directionPlayer2 = -speed
    directionBall = pygame.Vector2(speed * (3/5), speed * (3/5))
    positionPlayer1 = pygame.Vector2(margin["left"] + 25, screen.get_height() / 2)
    positionPlayer2 = pygame.Vector2(screen.get_width() - margin["right"] - 16 - 25, screen.get_height() / 2)
    positionBall = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    font = pygame.font.Font(None, 50)
    pointsText = font.render((str(points["player1"]) + " - " + str(points["player2"])), 1, "white")
    startText = font.render("Press space to start", 1, "white")
    centerPoints = pointsText.get_rect()
    centerPoints.centerx = screen.get_width() // 2
    centerPoints.centery = 15
    centerStart = startText.get_rect()
    centerStart.centerx = screen.get_width() // 2
    centerStart.centery = screen.get_height() // 2 - 30
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
    pygame.quit()
    if __name__ == "__main__":
        if isOnline == None or isOnline == "n":
            launcher()

def startGame():
    global root
    global isOnline
    width = int(inputWidth.get())
    height = int(inputHeight.get())
    speed = int(inputSpeed.get())
    root.destroy()
    if isOnline == None or isOnline == False:
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
    root.attributes('-topmost', True)
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
    def baseVariables():
        global start, running, points, positionPlayer1, directionPlayer1, positionPlayer2, directionPlayer2, positionBall, directionBall
        from pygame import Vector2
        #Standart values
        speed = 5
        margin = {"left":5, "right": 5}
        height, width = 500, 500
        #Base values
        start = False
        running = True
        points = {"player1" : 0, "player2" : 0}
        directionPlayer1 = speed
        directionPlayer2 = -speed
        directionBall = Vector2(speed * (3/5), speed * (3/5))
        positionPlayer1 = Vector2(margin["left"] + 25, height / 2)
        positionPlayer2 = Vector2(width - margin["right"] - 16 - 25, height/ 2)
        positionBall = Vector2(width / 2, height / 2)

    def host(width, height, speed):
        import threading
        import socket
        hostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostIP = socket.gethostbyname(socket.gethostname())
        hostPort = 50574
        hostData = hostIP, hostPort
        hostSocket.bind(hostData)
        print("\nTCP host up and listening")
        print(f"Host ip is: {hostIP}\nHost port is: {hostPort}")
        hostSocket.listen(2)
        print("\nWaiting for a connection...\n")
        hostWaiting = True
        while hostWaiting:
            clientSocket, clientData = hostSocket.accept()
            print(clientData[0] + " is trying to connect.\n")
            acceptConnection = input("Accept this connection (Y/n)? ").lower()
            if acceptConnection == "y":
                print("Connected by: " + clientData[0])
                clientSocket.send(b"Connection confirmation!")
                hostWaiting = False
            else:
                print("Connection rejected!")
                clientSocket.close()
        clientSocket.send(f"width={width}, height={height}, speed={speed}".encode())
        gameThread = threading.Thread(target=gamePong, args=(width, height, speed))
        dataThread = threading.Thread(target=online.hostSendData, args=(clientSocket,))
        online.baseVariables()
        gameThread.start()
        while gameThread.is_alive():
            dataThread.start()
            dataThread.join()
        hostSocket.close()
        print("End of connection!")

    def hostSendData(socket):
        global start, running, points, positionPlayer1, directionPlayer1, positionPlayer2, directionPlayer2, positionBall, directionBall
        socket.send(str(start).encode())
        socket.send(str(running).encode())
        socket.send((str(points["player1"]) + "," + str(points["player2"])).encode())
        socket.send(str(positionPlayer1.y).encode())
        socket.send(str(directionPlayer1).encode())
        socket.send((str(positionBall.x) + "," + str(positionBall.y)).encode())
        socket.send((str(directionBall.x) + "," + str(directionBall.y)).encode())
        start = socket.recv(1024).decode('utf-8') == "True"
        running = socket.recv(1024).decode('utf-8') == "True"
        positionPlayer2.y = int(socket.recv(1024).decode('utf-8'))
        directionPlayer2 = int(socket.recv(1024).decode('utf-8'))

    def client():
        import threading
        import socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientIP = socket.gethostbyname(socket.gethostname()) 
        print(f"Client ip is: {clientIP}")
        hostIP = input("Enter the host's ip: ")
        hostPort = 50574 #Standar port
        hostData = hostIP, hostPort
        clientSocket.connect(hostData)
        clientWaiting = True
        #RECIEVE CONFIRMATION DATA
        while clientWaiting:
            data = clientSocket.recv(1024).decode("utf-8")
            if data == "Connection confirmation!":
                print(f"Sucessfully connected to {hostIP}!")
                width, height, speed = None, None, None
                while width == None or height == None or speed == None:
                    print("Waiting for data")#TODO: MAYBE DELETE AFTER
                    data = clientSocket.recv(1024).decode("utf-8")
                    data = data.split(", ")
                    if len(data) == 3:
                        if data[0].startswith("width="):
                            width = int(data[0].split("=")[1])
                        if data[1].startswith("height="):
                            height = int(data[1].split("=")[1])
                        if data[2].startswith("speed="):
                            speed = int(data[2].split("=")[1])
                clientWaiting = False
        gameThread = threading.Thread(target=gamePong, args=(width, height, speed))
        dataThread = threading.Thread(target=online.clientSendData, args=(clientSocket,))
        online.baseVariables()
        gameThread.start()
        while gameThread.is_alive():
            dataThread.start()
            dataThread.join()
        clientSocket.close()
        print("End of connection!")

    def clientSendData(socket):
        global start, running, points, positionPlayer1, directionPlayer1, positionPlayer2, directionPlayer2, positionBall, directionBall
        start = socket.recv(1024).decode('utf-8') == "True"
        running = socket.recv(1024).decode('utf-8') == "True"
        temporalPoints = socket.recv(1024).decode('utf-8').split(",")
        points["player1"] = int(temporalPoints[0])
        points["player2"] = int(temporalPoints[1])
        positionPlayer1.y = int(socket.recv(1024).decode('utf-8'))
        directionPlayer1 = int(socket.recv(1024).decode('utf-8'))
        temporalPositionBall = socket.recv(1024).decode('utf-8').split(",")
        positionBall.x = int(temporalPositionBall[0])
        positionBall.y = int(temporalPositionBall[1])
        temporalDirectionBall = socket.recv(1024).decode('utf-8').split(",")
        directionBall.x = int(temporalDirectionBall[0])
        directionBall.y = int(temporalDirectionBall[1])
        socket.send(str(start).encode())
        socket.send(str(running).encode())
        socket.send(str(positionPlayer2.y).encode())
        socket.send(str(directionPlayer2).encode())

stringToBoolean ={"n": False, "y": True}
while __name__ == "__main__":
    isOnline = stringToBoolean[input("Online (Y/n)? ").lower()]
    if isOnline == True:
        hostOrClient = input("Host or client (H/c)? ").lower()
        if hostOrClient == "h":
            launcher()
        elif hostOrClient == "c":
            online.client()
    elif isOnline == "n":
        launcher()