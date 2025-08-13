# MUNCHデータセットからSFT用データを生成

このプロジェクトは、[MUNCH (Metaphor Understanding Challenge) データセット](https://github.com/xiaoyuisrain/metaphor-understanding-challenge.git)から、大規模言語モデルのSupervised Fine-Tuning (SFT)用データを生成するためのツールです。

## 概要

MUNCHデータセットは、大規模言語モデルの比喩理解能力をテストするためのデータセットです。このツールは、以下の2つの主要タスクからSFT用データを生成します：

1. **Paraphrase judgement（言い換え判定）**
   - Word judgement（単語判定）
   - Sentence judgement（文判定）

2. **Paraphrase generation（言い換え生成）**

## 生成されるSFTデータの形式

生成されるSFTデータは以下の形式になります：

```json
{
  "instruction": "タスクの説明と入力文",
  "input": "",
  "output": "期待される回答"
}
```

### 例：単語判定タスク

```json
{
  "instruction": "Choose the word(s) that can replace the highlighted word in the given sentence without changing the meaning of the sentence.\n\nSentence: While he suggests in apocalyptic *tones* in The Problem of Method that this process of self-consciousness is at last beginning to take place...\nOption A: language\nOption B: speeches\nOption C: Both Option A and Option B\nOption D: Neither Option A nor Option B\nCorrect answer:",
  "input": "",
  "output": "Option A"
}
```

### 例：言い換え生成タスク

```json
{
  "instruction": "Paraphrase the given sentence by substituting the highlighted word with another word. The substitution should be a single word.\n\nSentence: Latest corporate unbundler reveals laid-back <b>approach</b>: Roland Franklin, who is leading a 697m pound break-up bid for DRG, talks to Frank Kane\nParaphrase:",
  "input": "",
  "output": "Latest corporate unbundler reveals laid-back method: Roland Franklin, who is leading a 697m pound break-up bid for DRG, talks to Frank Kane"
}
```

## インストール

必要な依存関係は標準ライブラリのみです：

```bash
# 追加のインストールは不要
python main.py
```

## 使用方法

### 基本的な使用方法

```python
from main import MUNCHSFTDataGenerator

# データジェネレーターを初期化
generator = MUNCHSFTDataGenerator()

# 全てのタスクのSFTデータを生成
generator.generate_all_sft_data()
```

### 特定のタスクのみを生成

```python
# 単語判定タスクのみ
generator.generate_word_judgement_data(
    "tasks/word_judge.json",
    "word_judge_sft.json"
)

# 文判定タスクのみ
generator.generate_sentence_judgement_data(
    "tasks/sent_judge_implicit.json",
    "sent_judge_implicit_sft.json"
)

# 言い換え生成タスクのみ
generator.generate_paraphrase_generation_data(
    "tasks/generation.json",
    "correct_answers/for_generation.csv",
    "generation_sft.json"
)
```

### カスタム出力ディレクトリ

```python
# カスタム出力ディレクトリを指定
generator.generate_all_sft_data(output_dir="my_sft_data")
```

## タスクの詳細

### 1. Word Judgement（単語判定）

ハイライトされた単語を、文の意味を変えずに置き換えることができる単語を選択するタスク。

**条件：**
- **Implicit**: 通常の文での単語置換
- **M-sent**: 比喩文での単語置換
- **M-word**: 比喩的に使用された単語の置換

**選択肢：**
- Option A: 最初の単語
- Option B: 2番目の単語
- Option C: 両方の単語
- Option D: どちらの単語でもない

### 2. Sentence Judgement（文判定）

与えられた文の適切な言い換えを選択するタスク。

**条件：**
- **Implicit**: 通常の文の言い換え判定
- **M-sent**: 比喩文の言い換え判定
- **M-word**: 比喩的に使用された単語を含む文の言い換え判定

**選択肢：**
- Option A: 最初の言い換え
- Option B: 2番目の言い換え
- Option C: 両方の言い換え
- Option D: どちらの言い換えでもない

### 3. Paraphrase Generation（言い換え生成）

ハイライトされた単語を別の単語で置き換えて、文の言い換えを生成するタスク。

## 出力ファイル

`generate_all_sft_data()`を実行すると、以下のファイルが生成されます：

```
sft_data/
├── word_judge_sft.json          # 単語判定タスク
├── sent_judge_implicit_sft.json # 文判定（implicit）
├── sent_judge_msent_sft.json    # 文判定（metaphorical sentence）
├── sent_judge_mword_sft.json    # 文判定（metaphorical word）
├── generation_sft.json           # 言い換え生成タスク
└── all_sft_data.json            # 全データの統合版
```

## データの特徴

- **多様性**: ニュース、文学、学術文書など様々なジャンルの文を含む
- **比喩理解**: 比喩的な表現の理解を促進するデータ
- **言語的複雑性**: 様々な難易度レベルのタスク
- **人間注釈**: 人間による高品質な注釈データ

## 使用例

詳細な使用例は `example_usage.py` を参照してください：

```bash
python example_usage.py
```

## 注意事項

1. **オプションのシャッフル**: 選択肢は毎回ランダムにシャッフルされます
2. **データの整合性**: 元のMUNCHデータセットの構造に依存します
3. **エンコーディング**: UTF-8エンコーディングを使用します
4. **メモリ使用量**: 大規模なデータセットの場合、十分なメモリが必要です

## ライセンス

このプロジェクトは、元のMUNCHデータセットと同じライセンス（CC-BY-4.0）に従います。

## 貢献

バグ報告や機能改善の提案は、GitHubのIssueでお知らせください。

## 参考文献

- [MUNCH: Metaphor Understanding Challenge Dataset](https://github.com/xiaoyuisrain/metaphor-understanding-challenge.git)
- [Supervised Fine-Tuning (SFT) for Language Models](https://arxiv.org/abs/2004.10213)
