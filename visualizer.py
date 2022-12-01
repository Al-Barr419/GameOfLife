

def create_visualization(Parm, pProp):
    """
    with Screen() as scr:
        for val in Parm:
            coler = (1, 0, 0)
            if str(val) == "A(Barb,Barb,Barb)":
                continue
            if Parm[val]:
                coler = 0,1,0
            time = int(val.time)
            row = int(val.row)
            col = int(val.col)
            scr.high.draw.rect((5*(row)+40*time, 5*col), (5 + 5*(row)+40*time, 5 + 5*col), color = coler)
        pause()
    """
    '''
    print(Parm.keys())
    for ttime in range(1):
        for trow in range(3):
            for tcol in range(3):
                time = str(ttime)
                row = str(trow)
                col = str(tcol)
                print(" A("+time+","+row+","+col+") =" + Parm["A("+time+","+row+","+col+")"], end=" ")
    '''
    if Parm != None:
        for val in pProp:
            for key in val:
                for boob in key:
                    if Parm[boob]:
                        print("T", end=" ")
                    else:
                        print("F", end=" ")
                    #print(str(Parm[boob]), end=" ")
                print("\n")
            print("\n\n")


    print("   Solution: %s" % Parm)
