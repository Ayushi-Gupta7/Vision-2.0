import gym
import vision_arena
import time
import pybullet as p
import pybullet_data
import cv2
import numpy as np
import os
import math
import cv2.aruco as aruco

def Thresh2(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
##    cv2.imshow('hsv',hsv)
    threshY = cv2.inRange(hsv, Y[0], Y[1])
    threshR = cv2.inRange(hsv, R[0], R[1])
    thresh = cv2.bitwise_or(threshR, threshY)
##    cv2.imshow('threshY',threshY)
##    cv2.imshow('threshR',threshR)
##    cv2.imshow('thresh',thresh)
    imgY = cv2.bitwise_and(frame, frame, mask=threshY)
    imgR = cv2.bitwise_and(frame, frame, mask=threshR)
    img = cv2.bitwise_and(frame, frame, mask=thresh)
##    cv2.imshow('imgY',imgY)
##    cv2.imshow('imgR',imgR)
    cv2.imshow('img2',img)


##    contoursR,hR = cv2.findContours(threshR,1,2)
##    contoursY,hY = cv2.findContours(threshY,1,2)
    contours,h = cv2.findContours(thresh,1,2)
    shapeDetection2(contours,'All')
##    shapeDetection(contoursR,'Red')
##    shapeDetection(contoursY,'Yellow')


def shapeDetection2(contours,color):
    for cnt in contours:
        epsilon = 0.02*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        M = cv2.moments(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        if M["m00"] != 0:
            cx=int(M["m10"]/M["m00"])
            cy=int(M["m01"]/M["m00"])
        cnx.append(cx)
        cny.append(cy)


def Thresh(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
##    cv2.imshow('hsv',hsv)
    threshY = cv2.inRange(hsv, Y[0], Y[1])
    threshR = cv2.inRange(hsv, R[0], R[1])
    thresh = cv2.bitwise_or(threshR, threshY)
##    cv2.imshow('threshY',threshY)
##    cv2.imshow('threshR',threshR)
##    cv2.imshow('thresh',thresh)
    imgY = cv2.bitwise_and(f, f, mask=threshY)
    imgR = cv2.bitwise_and(f, f, mask=threshR)
    img = cv2.bitwise_and(f, f, mask=thresh)
    cv2.imshow('imgY',imgY)
    cv2.imshow('imgR',imgR)
    cv2.imshow('img',img)

    contoursR,hR = cv2.findContours(threshR,1,2)
    contoursY,hY = cv2.findContours(threshY,1,2)
    contours,h = cv2.findContours(thresh,1,2)

    shapeDetection(contoursR,'Red')
    shapeDetection(contoursY,'Yellow')




def shapeDetection(contours,color):
    for cnt in contours:
        epsilon = 0.02*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        M = cv2.moments(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        cx=0
        cy=0
        if M["m00"] != 0:
            cx=int(M["m10"]/M["m00"])
            cy=int(M["m01"]/M["m00"])
        p=cy//50
        q=cx//50
        # centroidX[p][q]=cx
        # centroidY[p][q]=cy
##        print (len(approx))
        if len(approx)==3:
##             print (len(approx))
             print (color," triangle")
             if(color=='Red'):
                 b[p][q]=1
             else:
                 b[p][q]=4

        elif len(approx)==4:
##             print (len(approx))
             print (color, " square")
             if(color=='Red'):
                 b[p][q]=2
             else:
                 b[p][q]=5
        elif len(approx)>4 and len(approx)<10:
##             print (len(approx))
             print (color, " circle")
             if(color=='Red'):
                 b[p][q]=3
             else:
                 b[p][q]=6


def feed():
    f=env.camera_feed()
    f=cv2.resize(f,(450,450))
    return f

def adjacency(b):
    for r in range(9):
        for c in range(9):
            if(r<4):
                if(c!=8 and shape[r][c+1] and shape[r][c]):
                   b[r*9+c][r*9+c+1]=1
                if(c!=0 and shape[r+1][c] and shape[r][c] and (c>=4)):
                   b[r * 9 + c][(r + 1) * 9 + c] = 1
                if(r!=0 and shape[r-1][c] and shape[r][c] and (c<=4)):
                   b[r * 9 + c][(r - 1) * 9 + c] = 1
            elif((r==4)):
                if(c==0):
                    if (shape[r][c + 1] and shape[r][c]):
                        b[r * 9 + c][(r) * 9 + c + 1] = 1
                elif(c==8):
                    if (shape[r][c - 1] and shape[r][c]):
                        b[r * 9 + c][(r) * 9 + c - 1] = 1
                else:
                    if (shape[r][c - 1] and shape[r][c]):
                        b[r * 9 + c][(r) * 9 + c - 1] = 1;
                    if (shape[r][c + 1] and shape[r][c]):
                        b[r * 9 + c][(r) * 9 + c + 1] = 1;
                if (c < 4 and shape[r - 1][c] and shape[r][c]):
                    b[r * 9 + c][(r - 1) * 9 + c] = 1
                if (c > 4 and shape[r + 1][c] and shape[r][c]):
                    b[r * 9 + c][(r + 1) * 9 + c] = 1
            else:
                if (c != 0 and shape[r][c - 1] and shape[r][c]):
                    b[r * 9 + c][(r) * 9 + c - 1] = 1;
                if (r != 8 and shape[r + 1][c] and shape[r][c] and c >= 4):
                    b[r * 9 + c][(r + 1) * 9 + c] = 1;
                if (c != 8 and shape[r - 1][c] and shape[r][c] and c <= 4):
                    b[r * 9 + c][(r - 1) * 9 + c] = 1;
    for i in range(81):
        b[40][i]=0
    return b

def bfs(node,dice_shape,shape):
    for i in range(81):
        parent[i]=-1
        vis[i]=False
    q = []
    vis[node ]=True
    q.append(node)
    while True:
        vis[q[0]] = True;
        for i in range(81):
            if(b[q[0]][i] and (not vis[i])):
                parent[i]=q[0]
                vis[i]=True
                q.append(i)
        if(len(q) !=0):
            del q[0]
        print(q[0],'q')
        if(int(shape[int(q[0]/9)][q[0]%9]) == int(dice_shape)):
            node=q[0]
            break
        if(q[0]==40):
            node=40
            break


    path=[]
    x=q[0]
    path.append(q[0])
    while(x!=-1 and parent[x]!=-1):
        path.append(parent[x])
        x=parent[x]
    path.reverse()
    print(path)

    # while True:
    #     count=0
    #     # for i in range(len(path))
    #     #     if(int(shape[int(path[i]/9)][path[i]%9]) == int(dice_shape)):
    #     #         return path,node
    #
    #     return -1,path[path[0]]
    s=len(path)-1
    # print(int(s/9))
    # print(s%9)
    d=path[s]
    print (int(shape[int(d/9)][d%9]))
    print (int(dice_shape))
    if(int(shape[int(d/9)][d%9]) == int(dice_shape)):
        return path,node
    else:
        return -1,path[0]



def Position():
    while True:

        try:

            f=feed()
            aruco_dict=aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
            parameters=aruco.DetectorParameters_create()
            corners,ids,_=aruco.detectMarkers(f,aruco_dict,parameters=parameters)
            # cv2.imshow('f',f)
            #if (len(corners)!= 0):
                #print(corners)
            print(corners)
            # while True:
            #     if(len(corners)==0):
            #         print('not detected')
            #         p.stepSimulation()
            #         env.move_husky(0.7,-0.7,0.7,-0.7)
            #         # p.stepSimulation()
            #         # env.move_husky(5,-5,5,-5)
            #         # p.stepSimulation()
            #         # env.move_husky(-4,4,-4,4)
            #     else:
            #         break
            #x=0
            #while x<400:
                #x=x+1
                #p.stepSimulation()
                #env.move_husky(0.7,-0.7,0.7,-0.7)

            #env.move_husky(0,0,0,0)
            #time.sleep(0.5)
            print('Hi')
            centroid=(int((corners[0][0][0][0]+corners[0][0][1][0]+corners[0][0][2][0]+corners[0][0][3][0])/4),(int(corners[0][0][0][1]+corners[0][0][1][1]+corners[0][0][2][1]+corners[0][0][3][1])/4))
            vector_aruco=(int(corners[0][0][0][0]-corners[0][0][3][0]),int(corners[0][0][0][1]-corners[0][0][3][1]))
            print (vector_aruco)
            print(corners[0][0][0][0])
            print(corners[0][0][3][0])
            print(corners[0][0][0][1])
            print(corners[0][0][3][1])

            return ((vector_aruco),(centroid))
        except:
            print('not detected')
            for i in range(6):
                p.stepSimulation()
                env.move_husky(10,-10,10,-10)
                # p.stepSimulation()

            continue


def centroid_node_fun(path,q):
    node=path[q]
    q=q+1
    c=node%9
    r=node//9
    cx=centroidX[r][c]
    cy=centroidY[r][c]
    cent=[cx,cy]
    return cent

def theta(v_a,v_n):
    v2=complex(v_a[0],v_a[1])
    v1=complex(v_n[0],v_n[1])
    # v=[v1,v2]
    # theta=np.angle(v,deg=True)
    # print('theta',theta)
    # theta=int(theta[0]-theta[1])
    theta=np.angle(v2/v1,deg=True)
    print(theta)
    return theta


def align(angle):

    dist= distance(centroid_aruco,centroid_node)
    print('dist',dist)
    m=int(math.sqrt(dist))
    s=3+0.2*m
    # while True:
    # p.stepSimulation()
    # env.move_husky(5, 5, 5, 5)
    if dist<=min_distance:
        print('stop')
        env.move_husky(0,0,0,0)
        p.stepSimulation()
        # env.move_husky(0,0,0,0)
        # p.stepSimulation()


    if angle<10 and angle>-10 and dist>min_distance :
        #move_husky=frwd
        print('frwd')
        for i in range(30):
            env.move_husky(s,s,s,s)
            p.stepSimulation()
            # p.stepSimulation()
            # env.move_husky(50,50,50,50)

    if angle>=10  and dist>min_distance:
        #move_husky =left
        print('left')
        # for i in range(0,int(angle*0.5)):
        for i in range(20):
            env.move_husky(-s,s,-s,s)
            p.stepSimulation()
            # p.stepSimulation()
            # env.move_husky(-35,35,-35,35)


    if angle<=-10  and dist>min_distance:
        #move_husky=right
        print('right')
        # for i in range(0,int(angle*0.5)):
        for i in range(20):
            env.move_husky(s,-s,s,-s)
            p.stepSimulation()
            # p.stepSimulation()
            # env.move_husky(35,-35,35,-35)

def distance(a,b):
    dist=(a[0]-b[0])**2+(a[1]-b[1])**2
    return dist

if __name__=="__main__":
    # time.sleep(100)
    parent_path = os.path.dirname(os.getcwd())
    os.chdir(parent_path)
    env = gym.make("vision_arena-v0")
    # time.sleep(3)
    env.remove_car()
    time.sleep(0.5)
    f = env.camera_feed()
    f=cv2.resize(f,(450,450))
    # centroidX=np.zeros((9,9))
    # centroidY=np.zeros((9,9))
    Y=np.array([ [20, 100, 130], [35, 255, 255] ])
    R=np.array([ [0, 125, 125], [10, 255, 200] ])
    centroidX_o=np.zeros((9,9))
    centroidY_o=np.zeros((9,9))
    cnx=[]
    cny=[]
    Thresh2(f)
    cnx.sort()
    cny.sort()
    for i in range(4):
        centroidX_o[i][0]=cnx[i]
    for i in range(5,9):
        centroidX_o[i][0]=cnx[i-1]
        centroidX_o[0][1]=cnx[8]
        centroidX_o[4][1]=cnx[9]
        centroidX_o[8][1]=cnx[10]
    for i in range(9):
        centroidX_o[i][2]=cnx[11]
        centroidX_o[i][3]=cnx[18]
        centroidX_o[i][4]=cnx[23]
        centroidX_o[i][5]=cnx[29]
        centroidX_o[i][6]=cnx[34]
        centroidX_o[i][7]=cnx[41]
        centroidX_o[i][8]=cnx[44]
        centroidY_o[0][i]=cny[0]
        centroidY_o[1][i]=cny[8]
        centroidY_o[2][i]=cny[11]
        centroidY_o[3][i]=cny[18]
        centroidY_o[4][i]=cny[23]
        centroidY_o[5][i]=cny[29]
        centroidY_o[6][i]=cny[34]
        centroidY_o[7][i]=cny[41]
        centroidY_o[8][i]=cny[44]



    print(cnx)
    print(cny)
    for i in range(9):
        for j in range(9):
            centroidX_o[i][j]=centroidY_o[j][i]

    print('original image centroids detected')
    roi = cv2.selectROI(f)
    f = f[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    f=cv2.resize(f,(450,450))
    cv2.imshow('f',f)
    b=np.zeros((9,9))
    #  SIGN CONVENTION
    # 1- Red triangle
    # 2- Red SQuare
    # 3- Red circle
    # 4- Yellow triangle
    # 5- Yellow square
    # 6- Yellow circle
    # 7- Black arrow
    # 8- Home
    b[0][4] = b[4][0] = b[8][4] = b[4][8] =7
    b[4][4] = 8
    ##cv2.waitKey(0)
    ##cv2.destroyAllWindows()
    ##height, width = f.shape[:2]
    ##print(height)
    ##print(width)



    Thresh(f)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(b)
    # centroidX[0][4]=centroidX[4][4]=centroidX[8][4]=centroidX[1][4]
    # centroidX[4][0]=centroidX[3][0]
    # centroidX[4][8]=centroidX[3][8]
    # centroidY[0][4]=centroidY[0][0]
    # centroidY[4][4]=centroidY[4][0]=centroidY[4][8]=centroidY[4][1]
    # centroidY[8][4]=centroidY[8][0]
    # print('c_i',centroidX)
    # print('ci',centroidY)

    # np.save('shape.npy', b)
    # np.save('centroidX.npy', centroidX)
    # np.save('centroidY.npy', centroidY)
    env.respawn_car()
    time.sleep(0.5)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # time.sleep(100)

    # parent_path = os.path.dirname(os.getcwd())
    # os.chdir(parent_path)
    # env = gym.make("vision_arena-v0")
    # time.sleep(3)
    shape=np.copy(b)
    centroidX=np.copy(centroidX_o)
    centroidY=np.copy(centroidY_o)
    print(shape)
    print(centroidX,"centroidX")
    print(centroidY,"centroidY")
    b = np.zeros((81, 81))
    b = adjacency(b)
    env.camera_feed()
    start = input('Enter 1 or 2 or 3 or 4:')
    b[38][39]=b[39][38]=b[22][31]=b[31][22]=b[41][42]=b[42][41]=b[58 ][49]=b[49][58]=0
    if(start == '2'):
        posX=4
        posY=0
        # b[38][39]=b[39][38]=1
    ##    b[36][37]=b[37][36]=0
    elif(start == '1'):
        posX=0
        posY=4
        # b[22][31]=b[31][22]=1
    ##    b[4][13]=b[13][4]=0
    elif(start == '3'):
        posX=4
        posY=8
        # b[41][42]=b[42][41]=1
    ##    b[44][43]=b[43][44]=0
    elif(start == '4'):
        posX=8
        posY=4
        # b[58][49]=b[49][58]=1
    ##    b[67][76]=b[76][67]=0
    ##for i in range(81):
    ##    for j in range(81):
    ##        if(b[i][j]==1):
    ##
    ##            print(i," " , j ," ",b[i][j])

    vis=np.zeros(81,dtype=bool)
    parent=np.zeros(81,dtype=int)
    # dice_shape_no=input('enter dice shape no')
    node=posX*9+posY
    dikt={
       'TY':4,
       'CY':6,
       'SY':5,
       'TR':1,
       'CR':3,
       'SR':2
    }
    # for i in range(10):
    count=0
    while(node!=40):
        count=count+1
        dice=env.roll_dice()
        print(dice,'dice')
        dice_shape_no=int(dikt[dice])
        if(count>3):
                if(start == '2'):
                    posX=4
                    posY=0
                    b[38][39]=1
                    b[36][27]=0
                    b[38][29]=0
                    b[39][40]=1
                ##    b[36][37]=b[37][36]=0
                elif(start == '1'):
                    posX=0
                    posY=4
                    b[22][31]=1
                    b[4][5]=0
                    b[22][23]=0
                    b[31][40]=1
                ##    b[4][13]=b[13][4]=0
                elif(start == '3'):
                    posX=4
                    posY=8
                    b[42][41]=1
                    b[44][53]=0
                    b[42][51]=0
                    b[41][40]=1

                ##    b[44][43]=b[43][44]=0
                elif(start == '4'):
                    posX=8
                    posY=4
                    b[58][49]=1
                    b[76][75]=0
                    b[58][57]=0
                    b[49][40]=1
        ##dice_shape=input('dice_shape')
        if(node==31 or node==39 or node==41 or node==49):
            dice_shape_no=8

        path,node=bfs(node,dice_shape_no,shape)
        print('bfs',path)
        if(path==-1):
            continue
        input('Press enter to continue')
        min_distance=200
        # while True:
        #     p.stepSimulation()
        #     env.move_husky(5, 5, 5, 5)
        for q in range(1,len(path)):
            centroid_node=centroid_node_fun(path,q)

            while True:
                    # cap = cv2.VideoCapture(1)
                    # _,f = cap.read()
                    # roi = cv2.selectROI(f)
                    # f = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                    # f=cv2.resize(f,(450,450))
                    ##cv2.imshow("f",f)
                    #roll-dice
                    f=feed()

                    vector_aruco,centroid_aruco=Position()
                    vector_node=(int(centroid_node[0]-centroid_aruco[0]),int(centroid_node[1]-centroid_aruco[1]))
                    print('nodevector',vector_node)

                    ang=theta(vector_aruco,vector_node)
                    print(ang)
                    dist= distance(centroid_aruco,centroid_node)

                    align(ang)
                    # env.move_husky(0,0,0,0)
                    # p.stepSimulation()
                    #
                    # time.sleep(0.05)
                    print(ang," ",centroid_node)
                    print(centroid_aruco,'centroid_a')
                    if dist<=min_distance:
                        node=path[q]
                        print('stop')
                        env.move_husky(0,0,0,0)
                        p.stepSimulation()
                        break

    if(node==40):
        print('Completed')
