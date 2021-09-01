import threading
from multiprocessing.dummy  import Pool
import multiprocessing
import time
from datetime import datetime,timezone,timedelta
import math
# ---------------------------------------------------------------------------------------------------------
def ReadFile( fileName ) :

    fileName = fileName + ".txt"
    with open(fileName, 'r') as f:
        content_list = f.read().splitlines()
    f.close()
    return content_list

def Method1( list1, fileName ) : # BubbleSort1
    time_start = time.time() # 開始計時

    for i in range ( len(list1) ) :
        for j in range ( len(list1)-1, i, -1 ) :
            if ( list1[j] < list1[j-1] ) :
                list1[j], list1[j - 1] = list1[j-1],  list1[j] # SWAP

    time_end = time.time() # 結束計時
    cpu_time = time_end - time_start
    fileName = fileName + "_output1.txt"
    with open(fileName, 'w') as f:
        f.write( "Sort : \n" )
        for i in list1 :
            f.write( str(i) ) # write只能寫string
            f.write("\n")

        dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
        dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
        # print('%s'%(dt2))
        # output_time = str(result.tm_year) + "-" + str(result.tm_mon ) + "-" + str(result.tm_mday) + " " + str(result.tm_hour) + ":" + str(result.tm_min) + ":" + str(result.tm_sec)
        output_time = str(dt2)
        f.write( "CPU Time : ")
        f.write( str(cpu_time) )
        f.write( "\n" )
        f.write( "Output Time : ") # 2021-03-28 01:59:22.409593+08:00
        f.write( output_time )

    f.close()
# ---------------------------------------------------------------------------------------------------------------
# def BubbleSort( inputs ) : # list, start, end
#     list2 = inputs[0]
#     start = inputs[1]
#     end = inputs[2]

#     i = start 
#     while ( i < end ) :
#         j = end - 1
#         while ( j > start ) :
#             if ( list2[j] < list2[j-1] ) :
#                 list2[j], list2[j-1] = list2[j-1], list2[j]
            
#             j = j - 1

#         i = i + 1
    

#     return list2[start:end]

def Merge(list_mg, start, mid, end) :
    L = list_mg[start:mid+1]
    R = list_mg[mid+1:end+1]
    L.append(-1)
    R.append(-1)
    i = 0
    j = 0
    k = start
    while ( k < end+1 ) :
        if ( L[i] <= R[j] ) :
            if ( L[i] == -1 ) :
                list_mg[k] = R[j]
                j = j + 1 
            else :
                list_mg[k] = L[i]
                i = i + 1 
        else :
            if ( R[j] == -1 ) :
                list_mg[k] = L[i]
                i = i + 1 
            else :
                list_mg[k] = R[j]
                j = j + 1 
        k = k + 1

# def MergeSort( inputs ) : #list_mg, start, end
#     # start = 0 
#     # end = len(list_mg) - 1
#     list_mg = inputs[0]
#     start = inputs[1]
#     end = inputs[2]

#     if ( start < end ) :
#         mid = int( (start + end ) / 2 )
#         inputs = [list_mg, start, mid]
#         MergeSort( inputs ) #start~mid
#         inputs = [list_mg, mid+1, end]
#         MergeSort( inputs ) # mid+1~end-1(因為從0開始)
#         Merge(list_mg, start, mid, end )
    
#     return list_mg

def Output( fileName, list_to_print, number, cpu_time, output_time ) :
    fileName = fileName + "_output" + number + ".txt"
    with open(fileName, 'w') as f:
        f.write( "Sort : \n" )
        for i in list_to_print :
            f.write( str(i) ) # write只能寫string
            f.write("\n")

        # result = time.localtime(time_end)
        # output_time = str(result.tm_year) + "-" + str(result.tm_mon ) + "-" + str(result.tm_mday) + " " + str(result.tm_hour) + ":" + str(result.tm_min) + ":" + str(result.tm_sec)
        f.write( "CPU Time : ")
        f.write( str(cpu_time) )
        f.write( "\n" )
        f.write( "Output Time : ") # 2021-03-28 01:59:22.409593+08:00
        f.write( output_time )

    f.close()

def Method2( list2, fileName, k ) :
    time_start = time.time() # 開始計時
    start = [] # start index
    end = [] # end index 
    size = int( len(list2) / k )
    list_to_Merge = []  
    pool = Pool(k) # 建立 k 個子執行緒
    # threads = []
    inputs = []
    i = 0
    start.append(0)
    for i in range(k): # 建立 k 個子執行緒
        end.append(start[i] + size) 
        if ( i+1 == k ) :
            end[i] = len(list2)

        # requests = makeRequests(target = BubbleSort, args = (list2, start[i], end[i] ))
        # threads.append(threading.Thread(target = BubbleSort, args = (list2, start[i], end[i] )))
        # threads[i].start()
        # pool.map(target = BubbleSort, args = (list2, start[i], end[i] ))
        inputs.append([list2, start[i], end[i]])

        list_to_Merge.append( list2[start[i]:end[i]] ) # 取到end前一個

        start.append(end[i]) 

    list_to_Merge = pool.map(BubbleSort_Procress, inputs)
    # 等待所有子執行緒結束
    # for i in range(k):
        # threads[i].join()
    # pool.wait()

    # threads = []
    inputs = []
    i = 0
    while (len(list_to_Merge) != 1 )  :
        list_mg = list_to_Merge[0] + list_to_Merge[1] 
        # threads.append( threading.Thread( target = MergeSort, args = ( list_mg, 0, len(list_mg)-1 ) ) )
        # threads[i].start()
        inputs.append([list_mg, 0, len(list_mg)-1])

        list_to_Merge.append( list_mg ) 

        i = i + 1
        if ( len(list_to_Merge) >= 3 ) :
            list_to_Merge = list_to_Merge[2:]

    # 等待所有子執行緒結束
    # for j in range(i):
    #     threads[j].join()
    list_to_Output = pool.map(MergeSort_Process, inputs)

    time_end = time.time() # 結束計時
    cpu_time = time_end - time_start
    # result = time.localtime(time_end)
    # output_time = str(result.tm_year) + "-" + str(result.tm_mon ) + "-" + str(result.tm_mday) + " " + str(result.tm_hour) + ":" + str(result.tm_min) + ":" + str(result.tm_sec)
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    # print('%s'%(dt2))
    # output_time = str(result.tm_year) + "-" + str(result.tm_mon ) + "-" + str(result.tm_mday) + " " + str(result.tm_hour) + ":" + str(result.tm_min) + ":" + str(result.tm_sec)
    output_time = str(dt2)
    # l = []
    # for u in list_to_Merge :
    #     l = l + u
    Output( fileName, list_to_Output[len(list_to_Output)-1], "2", cpu_time, output_time )
    #Output( fileName, list_to_Merge[0], "2", cpu_time, output_time )
# -----------------------------------------------------------------------------------------------------------------
def BubbleSort_Procress( inputs ) :
    list3 = inputs[0]
    start = inputs[1]
    end = inputs[2]
    # print("first: ", list3 )
    i = start 
    while ( i < end ) :
        j = end - 1
        while ( j > start ) :
            if ( list3[j] < list3[j-1] ) :
                list3[j], list3[j-1] = list3[j-1], list3[j]
            
            j = j - 1

        i = i + 1
    
    # print(list3[start:end])
    return list3[start:end]

def Merge_Process(list_mg, start, mid, end) :
    L = list_mg[start:mid+1]
    R = list_mg[mid+1:end+1]
    L.append(-1)
    R.append(-1)
    i = 0
    j = 0
    k = start
    while ( k < end+1 ) :
        if ( L[i] <= R[j] ) :
            if ( L[i] == -1 ) :
                list_mg[k] = R[j]
                j = j + 1 
            else :
                list_mg[k] = L[i]
                i = i + 1 
        else :
            if ( R[j] == -1 ) :
                list_mg[k] = L[i]
                i = i + 1 
            else :
                list_mg[k] = R[j]
                j = j + 1 
        k = k + 1
    # return list_mg

def MergeSort_Process( inputs ) :

    list_mg = inputs[0]
    start = inputs[1]
    end = inputs[2]

    if ( start < end ) :
        mid = int( (start + end ) / 2 )

        temp_inputs = [list_mg, start, mid]
        MergeSort_Process( temp_inputs ) #start~mid

        temp_inputs = [list_mg, mid+1, end ]
        MergeSort_Process( temp_inputs ) # mid+1~end-1(因為從0開始)
        Merge_Process(list_mg, start, mid, end )
    
    # print(list_mg)
    return list_mg

def Method3(list3, fileName, k) :
    time_start = time.time() # 開始計時
    start = [] # start index
    end = [] # end index 
    size = int( len(list3) / k )
    list_to_Merge = []
    pool = multiprocessing.Pool()
    i = 0
    inputs = []
    start.append(0)
    for i in range(k):
        end.append(start[i] + size) 
        if ( i+1 == k ) :
            end[i] = len(list3)

        inputs.append([list3,start[i], end[i]])

        start.append(end[i]) 

    list_to_Merge = pool.map(BubbleSort_Procress, inputs)

    inputs = []

    while (len(list_to_Merge) != 1 )  :
        list_mg = list_to_Merge[0] + list_to_Merge[1]
        inputs.append([list_mg, 0, len(list_mg)-1] )

        
        list_to_Merge.append( list_mg ) 

        i = i + 1
        if ( len(list_to_Merge) >= 3 ) :
            list_to_Merge = list_to_Merge[2:]


    list_to_Output = pool.map(MergeSort_Process, inputs)
 
    time_end = time.time() # 結束計時
    cpu_time = time_end - time_start
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    # print('%s'%(dt2))
    # output_time = str(result.tm_year) + "-" + str(result.tm_mon ) + "-" + str(result.tm_mday) + " " + str(result.tm_hour) + ":" + str(result.tm_min) + ":" + str(result.tm_sec)
    output_time = str(dt2)

    Output( fileName, list_to_Output[len(list_to_Output)-1], "3", cpu_time, output_time )

# -----------------------------------------------------------------------------------------------------------------
def BubbleSort( list, start, end ) :
    i = start 
    while ( i < end ) :
        j = end - 1
        while ( j > start ) :
            if ( list[j] < list[j-1] ) :
                list[j], list[j-1] = list[j-1], list[j]
            
            j = j - 1

        i = i + 1


def MergeSort( list_mg, start, end ) :
    # start = 0 
    # end = len(list_mg) - 1
    if ( start < end ) :
        mid = int( (start + end ) / 2 )
        MergeSort( list_mg, start, mid ) #start~mid
        MergeSort( list_mg, mid+1, end ) # mid+1~end-1(因為從0開始)
        Merge(list_mg, start, mid, end )

def Method4( list4, fileName, k ) :
    time_start = time.time() # 開始計時
    start = [] # start index
    end = [] # end index 
    size = int( len(list4) / k )
    list_to_Merge = []
    i = 0
    start.append(0)
    for i in range(k):
        end.append(start[i] + size) 
        if ( i+1 == k ) :
            end[i] = len(list4)

        BubbleSort(list4,start[i], end[i])
        list_to_Merge.append( list4[start[i]:end[i]] )
        start.append(end[i]) 

  

    while (len(list_to_Merge) != 1 )  :
        list_mg = list_to_Merge[0] + list_to_Merge[1]
      
        list_to_Merge.append( list_mg ) 
        MergeSort(list_mg, 0, len(list_mg)-1 )

        if ( len(list_to_Merge) >= 3 ) :
            list_to_Merge = list_to_Merge[2:]


    # list_to_Output = pool.map(MergeSort_Process, inputs)
 
    time_end = time.time() # 結束計時
    cpu_time = time_end - time_start
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    # print('%s'%(dt2))
    # output_time = str(result.tm_year) + "-" + str(result.tm_mon ) + "-" + str(result.tm_mday) + " " + str(result.tm_hour) + ":" + str(result.tm_min) + ":" + str(result.tm_sec)
    output_time = str(dt2)
    Output( fileName,list_mg, "4", cpu_time, output_time )

#-----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print( "*********************************" )
    print( "*********************************" )
    print( "**********    歡迎光臨    *********" )
    print( "*******   OS HomeWork ONE  ******" )
    print( "*********************************" )
    print( "*********************************" )
    print( "*********************************" )
    fileName = input("請輸入檔案名稱")
    list = ReadFile( fileName )
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    for i in range( 0, len(list) ) :
        list1.append( int( list[i] ) )
        list2.append(int(list[i]))
        list3.append(int(list[i]))
        list4.append(int(list[i]))

    k = int( input( "請輸入要切的份數" ) )
    Method1( list1, fileName )
    Method2( list2, fileName, k )
    Method3( list3, fileName, k )
    Method4( list4, fileName, k )