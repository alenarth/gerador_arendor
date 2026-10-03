<div align="center">

# ⚔️ Gerador de Nomes de Árendor ⚔️

*Todo herói precisa de um nome. Toda cidade, de uma placa na estrada.*

**Nomes de personagens e de lugares para os povos de Árendor,
cada um na sua própria língua.**

</div>

---

## 📜 Como abrir

> **Precisa ter o [Python](https://www.python.org/downloads/) instalado.**
> Na instalação, marque a opção **"Add Python to PATH"**.

Dê **dois cliques** em **`Gerar Nomes.bat`**. Pronto, é só isso.

<sub>Se preferir o terminal: `python menu.py` dentro desta pasta.</sub>

---

## 🧭 Como usar o menu

```
==================================================
  GERADOR DE NOMES DE RPG
==================================================

  1. Nome de personagem (nome + sobrenome)
  2. Só o primeiro nome
  3. Nome de lugar
  4. Ver línguas e raças
  0. Sair
```

1. Escolha **o que** quer gerar.
2. Escolha **o povo** e o **gênero** (ou o **tipo de lugar**).
3. Receba **10 nomes** de uma vez.

Na tela de resultados:

| Tecla     | O que faz                                        |
|:---------:|--------------------------------------------------|
| **Enter** | Gera outros 10 com as mesmas escolhas            |
| **S**     | Salva a lista em `nomes_salvos.txt`              |
| **M**     | Volta ao menu principal                          |

> 💡 Em qualquer pergunta, **Enter** aceita a opção padrão e **V** volta ao menu.

---

## 🗺️ Os povos e suas línguas

| Povo                         | Língua         | Soa como…                         | Um lugar…        |
|------------------------------|----------------|-----------------------------------|------------------|
| 🧑 Humano                    | **Istralino**  | Rosalia, Yane, Peth               | Feliciantia      |
| 🧝 Elfo                      | **Elgaran**    | Lielor, Vand, Lion                | Fenriendor       |
| ⛏️ Anão                      | **Dornval**    | Grun, Borg, Grin                  | Balin-grim       |
| 🍀 Halfling                  | **Brambel**    | Corigold, Perrigold, Sambob       | Bramble          |
| ⚙️ Gnomo                     | **Fizzwick**   | Glimble, Pippeton, Cogswellette   | Bimgladgeton     |
| 🪓 Orc · Goblin              | **Djolgronin** | Kruthra, Vroma, Drugak            | Dol-Zan          |
| 🌸 Fae                       | **Aoslin**     | Liraelin, Obeth, Maberon          | Faelethelmound   |
| 🐉 Dragão                    | **Vethrix**    | Moraxa, Sarax, Aurdorax           | Aurgor           |
| 😈 Demônio                   | **Xarveth**    | Mal'ena, Zarvor'tha, Kael         | Malzar'narvor    |
| 🐺 Povo-bicho                | **Feran**      | Torenir, Venrir, Rarakelanar      | Kavrosanwed      |

### Tipos de lugar

🏰 Cidade · 🏘️ Vila · 🛖 Aldeia · 🛡️ Fortaleza · 🌲 Floresta · ⛰️ Montanha · 🌊 Rio
🗺️ Região · 🌄 Colina · 🏞️ Vale · ⛏️ Mina · 🕳️ Abismo · 👑 Trono

---

## 🔮 De onde vêm os nomes

Cada lista mistura três fontes:

- **Nomes inéditos**, criados a partir dos nomes do banco de Árendor, com a mesma "cara" de cada língua.
- **Nomes do banco**, escolhidos à mão para cada povo.
- **Nomes montados por sílabas**, com os sons típicos de cada língua.

Quanto mais nomes o banco tiver, melhores ficam os nomes inéditos.

---

## 🖋️ Para o mestre: aumentando o banco de nomes

Os nomes ficam em duas planilhas simples, que abrem no Excel ou no Bloco de Notas:

| Arquivo                          | Colunas                     | Exemplo de linha                     |
|----------------------------------|-----------------------------|--------------------------------------|
| `namegen/data/nomes_pessoais.csv`| `nome,lingua,raca,genero`   | `Thrag,djolgronin,orc,masculino`     |
| `namegen/data/nomes_lugares.csv` | `nome,lingua,raca,tipo`     | `Dol-Makjar,djolgronin,orc,cidade`   |

- **lingua:** `djolgronin`, `elgaran`, `dornval`, `istralino`, `brambel`, `fizzwick`, `aoslin`, `vethrix`, `xarveth` ou `feran`.
- **genero:** `masculino` ou `feminino`.
- **tipo:** um dos tipos de lugar acima, sem acento (`cidade`, `regiao`, `mina`…).

Acrescente as linhas, salve e abra o gerador de novo. Ele aprende com os nomes novos sozinho.

> ⚠️ Se uma linha usar uma língua que não existe, o gerador avisa qual linha está errada ao abrir.

---

<details>
<summary><b>🛠️ Para quem programa</b></summary>

<br>

Funciona offline, só com a biblioteca padrão do Python (3.8+).

```python
from namegen import NameGenerator, HybridGenerator

gen = NameGenerator(seed=42)
gen.generate_full_name("anao")["full_name"]          # nome + sobrenome
gen.generate_place_name("elf", "floresta")

hybrid = HybridGenerator()
hybrid.generate("halfling", method="markov", gender="feminino")
hybrid.generate_full_name("elfo", gender="feminino")["full_name"]
hybrid.generate_place("orc", "fortaleza", method="database")
```

| Método     | O que faz                                    |
|------------|----------------------------------------------|
| `syllable` | combina sílabas da língua                    |
| `markov`   | cria nomes novos no estilo do banco          |
| `database` | sorteia um nome pronto do banco              |
| `auto`     | mistura os três (é o que o menu usa)         |

Raças, tipos de lugar e gêneros aceitam inglês ou português
(`dwarf`/`anao`, `city`/`cidade`, `female`/`feminino`).

| Arquivo                     | Conteúdo                                         |
|-----------------------------|--------------------------------------------------|
| `menu.py`                   | o menu interativo                                |
| `namegen/generator.py`      | geradores (sílabas, Markov e híbrido)            |
| `namegen/database.py`       | leitura dos bancos `.csv`                        |
| `namegen/syllable_data.py`  | línguas, sílabas, sufixos e raça → língua        |

Chaves internas das línguas: `common` (Istralino), `elvish` (Elgaran),
`dwarvish` (Dornval), `halfling` (Brambel), `gnomish` (Fizzwick),
`orcish` (Djolgronin), `sylvan` (Aoslin), `draconic` (Vethrix),
`infernal` (Xarveth), `beastial` (Feran).

</details>

<div align="center">

---

*Que seus nomes ecoem pelas terras de Árendor.* 🗡️

</div>
