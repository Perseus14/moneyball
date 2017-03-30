import csv
import os
import numpy


def column(matrix, i):
    return [int(row[i]) for row in matrix]


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    #there are 616 players
    for i in range(1, 617):               
        rel_path = "Data/Players/player_{0}.csv".format(i)
        abs_file_path = os.path.join(script_dir, rel_path)
        f = csv.reader(open(abs_file_path, "rb"))
        data = []
        for row in f:
            data.append(row)    
        rel_path = ""
        if(int(data[1][5]) == 1):                                            
            rel_path = "Data/Processed/Goalkeepers/p_player_{0}.csv".format(i)
        elif(int(data[1][5]) == 2):                                            
            rel_path = "Data/Processed/Defenders/p_player_{0}.csv".format(i)
        elif(int(data[1][5]) == 3):                                            
            rel_path = "Data/Processed/Midfielders/p_player_{0}.csv".format(i)  
        else:                                            
            rel_path = "Data/Processed/Forwards/p_player_{0}.csv".format(i)                      
        abs_file_path = os.path.join(script_dir, rel_path)
        fw = csv.writer(open(abs_file_path, "wb+"))
        data[0].insert(-1, "average_points")
        fw.writerow(data[0])
        points = []
        stop = min(6, len(data)-1)
        for j in range(1, stop):
            row = data[j]
            #if minutes is not equal to 0
            if(int(row[28]) != 0):
                points.append(int(row[-1]))
        for j in range(stop, len(data)):           
            row = data[j][:]
            if(j == len(data)-1):
                for _ in range(28, 57):
                    row.append("")            
            for k in range(28, 56):  
                #compute running 5 average         
                no = stop - 1
                row[k] = numpy.mean(column(data[j-no : j], k))
            #calculate average points for last 5 games which played not actual 5 last games
            if(len(points) != 0):
                if(len(points) < 5):
                    avg_points = float(sum(points))/len(points)
                else:
                    avg_points = sum(points[-5 : ])/float(5)                                                   
                row.insert(-1, avg_points)
            else:
                row.insert(-1, 0)            
            fw.writerow(row) 
            #except last row
            if(j != len(data)-1):                            
                if(int(row[28]) != 0):
                    points.append(int(row[-1]))
        print "Processed player {0}".format(i)
