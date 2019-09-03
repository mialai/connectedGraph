#-*- coding: utf-8 -*-
# Author: mialai
# date :2019/8/28
"""
============================================
判断有向图的节点是否连通
method: 计算图的强连通图，然后缩点，单连通
input:  图节点的邻接边
output: 节点不连通信息
============================================
"""


import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt
import sys

#algo.DFS 输出结果
def dfs_out_put(graph):
    #graph info
    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())
    problemVertex=[]
    with open('result.disconnectionlist','w') as file:
        
        file.write("Number of nodes: %d\n" %num_nodes)
        file.write("Number of edges: %d\n" %num_edges)
        
        for i in range(1,num_nodes+1):
            
            out_degree = graph.out_degree(i)
            in_degree = graph.in_degree(i)
            if (out_degree==0 or in_degree==0):
                problemVertex.append(i)
            print("%d (%d,%d): "%(i,out_degree,in_degree),end="")
           
            file.write('%d (%d,%d): '%(i,out_degree,in_degree))
           
            for j in range(1,num_nodes+1):
                isConnected = nx.has_path(graph,i,j)
                if not isConnected:
                   
                    print(" %d"%j,end="")
                    file.write(" %d"%j)
            file.write("\n")
            print()

        print("Suggest to check points :"+str(problemVertex))
        file.write("Suggest to check points :"+str(problemVertex)+"\n")

#algo.Tarjan 输出结果
def tarjan_out_put(graph):
    #图信息
    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())
    
    #强连通图
    strongly_connected = list(nx.strongly_connected_components(graph))
    num_strongly_connected = len(strongly_connected)
    #强连通图（子图）的元素个数
    subgraph_length = [len(c) for c in strongly_connected]

    #缩点
    neighborlistStrong=[]
   
    DG = nx.DiGraph()

    for i in range(num_strongly_connected):

        mlist = list(strongly_connected[i])
    
        neighborlistOrigin=set()
        
        for j in mlist:

            temp = list(nx.neighbors(graph,j))
            
            for k in temp:

                 neighborlistOrigin.add(k)

        neighborlistStrong.append(neighborlistOrigin)

    for i in range(num_strongly_connected):
     
        c = []
       
        for j in range(num_strongly_connected):
            
            if i!=j:
                
                x =neighborlistStrong[i].intersection(strongly_connected[j]) 
               
                if len(x)!=0:
               
                    c.append(j+1)  
                    
        print("%d ===>"%(i+1),end="")
        print(c)
        for diEdge in c:
            if len(c)!=0:
                DG.add_edge(i+1,diEdge)
    

    
    #输出
    with open('result.disconnectionlist','w') as file:
        
        file.write("Number of nodes: %d\n" %num_nodes)

        file.write("Number of edges: %d\n" %num_edges)

        file.write("Number of strongly_connected: %d\n" %num_strongly_connected)

        file.write("the range of strongly_connected: "+str(subgraph_length)+"\n\n")
     

        for i in range(num_strongly_connected ):

            m = len(strongly_connected[i])

            mem_strongly_connected = list(strongly_connected[i])

            file.write("%d (%d): "%(i+1,m))

            for j in range(m):
                if ((j+1)%50)==0:
                     file.write("\n")
                else:
                     file.write(str(mem_strongly_connected[j])+" ")
            file.write("\n")   
                
                   
	 #   pos=nx.spring_layout(DG,iterations=100)
	
    nx.draw(DG,with_labels=True)
    plt.show()

def main():
	
	#建图
#    G = nx.read_adjlist("str",create_using=nx.DiGraph(),nodetype=int)
   
 #   scOutPut(G)
 
    G = nx.DiGraph()

    with open("graph_10_10","r") as file:

        for c in file.readlines():
			
            c_array = c.split(" ")
            
            if len(c_array)>1:
                
                for m in range(1,len(c_array)):
                    
                    G.add_edge(c_array[0],c_array[m])

    tarjan_out_put(G)       
        

if __name__=="__main__":
    time_start = time.time()
    main()

    time_end = time.time()

    print("total cost time:",time_end-time_start)
    with open('result.disconnectionlist','a') as file:
        file.write("total cost time:%f "%(time_end-time_start))