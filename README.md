# Enem 2017 Analysis
## Notebook para transformação de dados:
Contém notebook com transformações e modelagem em Source Code
Para rodar basta utilizar IDE ou ambiente com python 3.7 com as seguintes bibliotecas:
* ftplib any version
* pandas 0.23.4

Verificar path de arquivos, foi construído na minha máquina local portanto ao rodar será necessário alterar o path dos arquivos.
O mesmo se aplica para atualizar os dados no PowerBI.

## Visualização de Resultados

O arquivo .pbix encontra-se no link do google drive : https://drive.google.com/file/d/19UYzfIAgGDb8bkkbTuDWTVGfWdHhROux/view?usp=sharing

## Modelagem escolhida:

https://github.com/eleuuterio/enem_2017/blob/master/model%20schema.jpg?raw=true


Foram derivadas dimensões dos dados do Enem e foi utilizado uma dimensão pré-existente de localidades, o schema foi escolhido para dar flexibilidade às análises realizadas.
A nota geral do Enem é calculada através de uma medida no PowerBi para possibilitar o calculo em diferentes contextos.
O schema é um start schema, entretanto a dimensão estudante tem uma dimensão conectada a ela, utilizando conceitos de um schema Snowflake, pois essa configuração auxilia na confecção dos relatórios.

## Proposta de arquitetura AWS:

* EMR para landing de novos arquivos (imaginando que o volume dos dados não será suportado em um bucket S3
* Databricks para transformações
* RDS para armazenar os dados mestre e para carregar os dados de output ou RDS com dados mestre e podemos carregar os dados de output no EMR/S3 
* Conexão da ferramenta de visualização nas fontes de dados (dimensões direto do SQL não por tabelas e dados processados em arquivos ou SQL)

No caso as dimensões derivadas dos dados ou em mudanças nas dimensões, as dimensões derivadas tem que passar por processo de validação, para conferir se há mudanças nas dimensões. Em caso de mudança, se for necessário manter antigas versões das dimensões usar técnicas de slowly changing dimension a depender do tipo de mudança na dimensão e requerimentos sobre  versões anteriore.

No caso de dados do Enem eu sugiro overwrite em todas as dimensões derivadas e acredito que a dimensão utilizada(de local) caso venha a sofrer algumas mudança do tipo aumento da população e IDH, entre outros atributos numéricos, sugiro adicionar uma tabela de histórico para acompanhar as variações de valores. Acho improvável uma mudança na hierarquia de municípios, entretanto, caso ocorra, sugiro um a adição de um atributo de versão, para possibilitar checagem histórica correta.

PS: não conheço muito bem os serviços da AWS usei um comparativo com os da Azure, os quais conheço.
