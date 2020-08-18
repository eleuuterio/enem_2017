# Enem 2017 Analysis
## Notebook para transformação de dados:
Contém notebook com transformações e modelagem em Source Code
Para rodar basta utilizar IDE ou ambiente com python 3.7 com as seguintes bibliotecas:
* ftplib any version
* pandas 0.23.4

Verificar path de arquivos, foi construído na minha máquina local portanto ao rodar será necessário alterar o path dos arquivos.
O mesmo se aplica para atualizar os dados no PowerBI.

## Visualização de Resultados

O arquivo .pbix encontra-se no link do google drive : 

## Modelagem escolhida:

https://github.com/eleuuterio/enem_2017/blob/master/model%20schema.jpg?raw=true


Foram derivadas dimensões dos dados do Enem e foi utilizado uma dimensão pré-existente de localidades, o schema foi escolhido para dar flexibilidade às análises realizadas.
A nota geral do Enem é calculada através de uma medida no PowerBi para possibilitar o calculo em diferentes contextos.
O schema é um start schema, entretanto a dimensão estudante tem uma dimensão conectada a ela, utilizando conceitos de um schema Snowflake, pois essa configuração auxilia na confecção dos relatórios.
