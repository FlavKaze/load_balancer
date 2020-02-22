Para execução do script load_balancer.py, deve possuir um arquivo input.txt, com no mínimo três linhas com três números inteiros, sendo eles:  
3, para a primeira linha  
4, para a segunda linha e  
5, para a terceira linha  
Para as linhas seguintes, poderá inserir outros números inteiros.  

O número 3 representa o tamanho das tasks em ticks (>=1<=10>). O número 4 representa a quantidade de tasks que uma máquina pode executar simultaneamente (>=1<=10>).   
O número 5 representa as tasks que serão executadas no primeiro tick (5 tasks). 

Podendo inserir outros números inteiros nas linhas que representa os números de tasks, exemplo:   
4  
2  
1  
3  
0  
1  
0  
1  

E, para obter o resultado do script, basta executar o comando python3 load_balancer.py