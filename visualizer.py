def create_visualization(Parm, pProp):
    if Parm != None:
        for val in pProp:
            for key in val:
                for boob in key:
                    if Parm[boob]:
                        print("T", end=" ")
                    else:
                        print("F", end=" ")

                print("\n")
            print("\n\n")
    print("   Solution: %s" % Parm)
