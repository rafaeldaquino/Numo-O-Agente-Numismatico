# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Para que serve no Numo? |
|---------|---------|---------------------|
| `acervo-moedas.csv` | CSV | Base de dados para consultas de informações de moedas no acervo |
| `denominacoes.json` | JSON | Contextualizar historicamente e educar |
| `perfil-colecionador.json` | JSON | Personalizar as explicações sobre as dúvidas e necessidades de aprendizado do cliente |

## Estratégia de Integração

### Como os dados são carregados?

Os três arquivos são carregados por código no início da aplicação (CSV com Pandas, JSON nativo):

```python

import pandas as pd
import json

acervo       = pd.read_csv("./data/acervo_moedas.csv")
denominacoes = json.load(open("./data/denominacoes.json", encoding="utf-8"))["denominacoes"]
perfil       = json.load(open("./data/perfil_colecionador.json", encoding="utf-8"))
```

## Exemplo de Contexto Montado

> Exemplo real para a pergunta: "Me fale sobre a moeda de 40 Réis de 1823."

O contexto sintetiza apenas o que é relevante (economia de tokens), mas sem omitir nada que o agente precise para responder com segurança. 


```text
========================  CONTEXTO PARA O NUMO  ========================

[PERFIL DE ATENDIMENTO]
Tom: didático, paciente e acolhedor. Linguagem: português claro, sem
jargão. Formato: resposta curta, terminando com convite para aprofundar.

Formato Resposta:
[CAMADA 1 — DADOS DA MOEDA NO ACERVO]   (fonte: acervo_moedas.csv)

Descrição: 40 Réis 1823 - Brasil
País: Brasil    | Categoria: Imperial
Denominação: Réis    | Valor facial: 40
Ano: 1823
Metal: Cobre    | Casa da moeda: Casa da Moeda do Brasil
Conservação: MBC
Peso: 7,50 g    | Diâmetro: 32,0 mm    | Tiragem: 67.300
Quantidade no acervo: 1    | Localização: Caixa 1

[CAMADA 2 — HISTÓRIA DA DENOMINAÇÃO "Réis"]   (fonte: denominacoes.json)

Sistema monetário: Real (plural: Réis)
Região: Portugal e Brasil
Período aproximado: Idade Média (Portugal) até 1942 (Brasil)
Contexto: o real foi a unidade monetária de Portugal por séculos e
acompanhou a colonização; contava-se em milhares de réis (o 'mil-réis').
Transição: substituído pelo cruzeiro em 1942.
Curiosidade: a grafia '1$000' representava mil réis.



```


