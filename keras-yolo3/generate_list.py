print ("Insert number of files:")
size = int(input())
f = open("train.txt","w+")
for i in range (size):
    f.write("IMG_%04d\n" % (i))
f.close()