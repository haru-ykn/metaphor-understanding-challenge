import json
import csv
import random
from typing import List, Dict, Any, Tuple
import re

class MUNCHSFTDataGenerator:
    """MUNCHデータセットからSFT用データを生成するクラス"""
    
    def __init__(self):
        self.prompts = self._load_prompts()
        
    def _load_prompts(self) -> Dict[str, str]:
        """プロンプトファイルを読み込む"""
        prompts = {}
        
        # プロンプトファイルから各タスクのプロンプトを抽出
        prompt_text = """
## Paraphrase judgement
### Word judgement: Implicit
Choose the word(s) that can replace the highlighted word in the given sentence without changing the meaning of the sentence.

### Word judgement: M-sent
Choose the word(s) that can replace the highlighted word in the given metaphorical sentence without changing the meaning of the sentence.

### Word judgement: M-word
Choose the word(s) that can replace the highlighted metaphorically used word in the given sentence without changing the meaning of the sentence.

### Sentence judgement: Implicit
Choose the correct paraphrase(s) for the given sentence.

### Sentence judgement: M-sent
Choose the correct paraphrase(s) for the given metaphorical sentence.

### Sentence judgement: M-word
You are given a sentence where the highlighted word is metaphorically used. Choose the correct paraphrase(s) for the given sentence.

## Paraphrase generation
Paraphrase the given sentence by substituting the highlighted word with another word. The substitution should be a single word.
"""
        
        # 各タスクタイプに対応するプロンプトを設定
        prompts['word_judge_implicit'] = "Choose the word(s) that can replace the highlighted word in the given sentence without changing the meaning of the sentence."
        prompts['word_judge_msent'] = "Choose the word(s) that can replace the highlighted word in the given metaphorical sentence without changing the meaning of the sentence."
        prompts['word_judge_mword'] = "Choose the word(s) that can replace the highlighted metaphorically used word in the given sentence without changing the meaning of the sentence."
        prompts['sent_judge_implicit'] = "Choose the correct paraphrase(s) for the given sentence."
        prompts['sent_judge_msent'] = "Choose the correct paraphrase(s) for the given metaphorical sentence."
        prompts['sent_judge_mword'] = "You are given a sentence where the highlighted word is metaphorically used. Choose the correct paraphrase(s) for the given sentence."
        prompts['generation'] = "Paraphrase the given sentence by substituting the highlighted word with another word. The substitution should be a single word."
        
        return prompts
    
    def _extract_highlighted_word(self, sentence: str) -> str:
        """文からハイライトされた単語を抽出"""
        # <b>タグまたは*で囲まれた単語を抽出
        match = re.search(r'<b>(.*?)</b>|\*(.*?)\*', sentence)
        if match:
            return match.group(1) or match.group(2)
        return ""
    
    def _remove_highlight_tags(self, sentence: str) -> str:
        """ハイライトタグを削除"""
        # <b>タグまたは*を削除
        sentence = re.sub(r'<b>(.*?)</b>', r'\1', sentence)
        sentence = re.sub(r'\*(.*?)\*', r'\1', sentence)
        return sentence
    
    def _shuffle_options(self, options: List[str]) -> List[str]:
        """オプションをシャッフル"""
        shuffled = options.copy()
        random.shuffle(shuffled)
        return shuffled
    
    def generate_word_judgement_data(self, word_judge_file: str, output_file: str):
        """単語判定タスクのSFTデータを生成"""
        with open(word_judge_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        sft_data = []
        
        for item in data:
            sentence = item['s0']
            options = item['options']
            
            # ハイライトされた単語を抽出
            highlighted_word = self._extract_highlighted_word(sentence)
            if not highlighted_word:
                continue
            
            # 適切なオプションと不適切なオプションを分離
            apt_options = [opt['text'] for opt in options if opt['label'] == 'apt']
            inapt_options = [opt['text'] for opt in options if opt['label'] == 'inapt']
            
            if not apt_options or not inapt_options:
                continue
            
            # オプションをシャッフル
            all_options = apt_options + inapt_options
            shuffled_options = self._shuffle_options(all_options)
            
            # 正解を特定
            correct_answer = ""
            if len(apt_options) == 1 and len(inapt_options) == 1:
                if shuffled_options[0] in apt_options:
                    correct_answer = "Option A"
                else:
                    correct_answer = "Option B"
            elif len(apt_options) == 2:
                correct_answer = "Option C"
            else:
                correct_answer = "Option D"
            
            # プロンプトを構築
            prompt = f"{self.prompts['word_judge_implicit']}\n\nSentence: {sentence}\nOption A: {shuffled_options[0]}\nOption B: {shuffled_options[1]}\nOption C: Both Option A and Option B\nOption D: Neither Option A nor Option B\nCorrect answer:"
            
            sft_data.append({
                "instruction": prompt,
                "input": "",
                "output": correct_answer
            })
        
        # SFTデータを保存
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sft_data, f, ensure_ascii=False, indent=2)
        
        print(f"単語判定タスクのSFTデータを {len(sft_data)} 件生成しました: {output_file}")
    
    def generate_sentence_judgement_data(self, sent_judge_file: str, output_file: str):
        """文判定タスクのSFTデータを生成"""
        with open(sent_judge_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        sft_data = []
        
        for item in data:
            original_sentence = item['s0']
            options = item['options']
            
            # ハイライトされた単語を抽出
            highlighted_word = self._extract_highlighted_word(original_sentence)
            if not highlighted_word:
                continue
            
            # 適切なオプションと不適切なオプションを分離
            apt_options = [opt['text'] for opt in options if opt['label'] == 'apt']
            inapt_options = [opt['text'] for opt in options if opt['label'] == 'inapt']
            
            if not apt_options or not inapt_options:
                continue
            
            # オプションをシャッフル
            all_options = apt_options + inapt_options
            shuffled_options = self._shuffle_options(all_options)
            
            # 正解を特定
            correct_answer = ""
            if len(apt_options) == 1 and len(inapt_options) == 1:
                if shuffled_options[0] in apt_options:
                    correct_answer = "Option A"
                else:
                    correct_answer = "Option B"
            elif len(apt_options) == 2:
                correct_answer = "Option C"
            else:
                correct_answer = "Option D"
            
            # プロンプトを構築
            prompt = f"{self.prompts['sent_judge_implicit']}\n\nSentence: {original_sentence}\nOption A: {shuffled_options[0]}\nOption B: {shuffled_options[1]}\nOption C: Both Option A and Option B\nOption D: Neither Option A nor Option B\nCorrect answer:"
            
            sft_data.append({
                "instruction": prompt,
                "input": "",
                "output": correct_answer
            })
        
        # SFTデータを保存
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sft_data, f, ensure_ascii=False, indent=2)
        
        print(f"文判定タスクのSFTデータを {len(sft_data)} 件生成しました: {output_file}")
    
    def generate_paraphrase_generation_data(self, generation_file: str, correct_answers_file: str, output_file: str):
        """言い換え生成タスクのSFTデータを生成"""
        # 生成タスクのデータを読み込み
        with open(generation_file, 'r', encoding='utf-8') as f:
            generation_data = json.load(f)
        
        # 正解データを読み込み
        correct_answers = {}
        with open(correct_answers_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                idx = int(row['idx'])
                correct_answers[idx] = row['human_ans'].split()
        
        sft_data = []
        
        for item in generation_data:
            dataset_index = item['dataset_index']
            sentence = item['s0']
            
            # 正解が存在しない場合はスキップ
            if dataset_index not in correct_answers:
                continue
            
            # ハイライトされた単語を抽出
            highlighted_word = self._extract_highlighted_word(sentence)
            if not highlighted_word:
                continue
            
            # 正解の言い換えを取得（最初のものを使用）
            correct_paraphrases = correct_answers[dataset_index]
            if not correct_paraphrases:
                continue
            
            # プロンプトを構築
            prompt = f"{self.prompts['generation']}\n\nSentence: {sentence}\nParaphrase:"
            
            # ハイライトされた単語を正解の言い換えで置き換えた文を作成
            paraphrased_sentence = self._remove_highlight_tags(sentence).replace(highlighted_word, correct_paraphrases[0])
            
            sft_data.append({
                "instruction": prompt,
                "input": "",
                "output": paraphrased_sentence
            })
        
        # SFTデータを保存
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sft_data, f, ensure_ascii=False, indent=2)
        
        print(f"言い換え生成タスクのSFTデータを {len(sft_data)} 件生成しました: {output_file}")
    
    def generate_all_sft_data(self, output_dir: str = "sft_data"):
        """全てのタスクのSFTデータを生成"""
        import os
        
        # 出力ディレクトリを作成
        os.makedirs(output_dir, exist_ok=True)
        
        # 単語判定タスク（3つの条件）
        self.generate_word_judgement_data(
            "tasks/word_judge.json",
            f"{output_dir}/word_judge_sft.json"
        )
        
        # 文判定タスク（3つの条件）
        for condition in ['implicit', 'msent', 'mword']:
            self.generate_sentence_judgement_data(
                f"tasks/sent_judge_{condition}.json",
                f"{output_dir}/sent_judge_{condition}_sft.json"
            )
        
        # 言い換え生成タスク
        self.generate_paraphrase_generation_data(
            "tasks/generation.json",
            "correct_answers/for_generation.csv",
            f"{output_dir}/generation_sft.json"
        )
        
        # 全データを統合
        self._merge_all_sft_data(output_dir)
        
        print(f"\n全てのSFTデータの生成が完了しました。出力先: {output_dir}")
    
    def _merge_all_sft_data(self, output_dir: str):
        """全てのSFTデータを統合"""
        import os
        
        all_data = []
        
        # 各ファイルからデータを読み込み
        for filename in os.listdir(output_dir):
            if filename.endswith('_sft.json'):
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_data.extend(data)
        
        # 統合データを保存
        merged_file = os.path.join(output_dir, "all_sft_data.json")
        with open(merged_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        print(f"統合されたSFTデータを {len(all_data)} 件保存しました: {merged_file}")
        
        # 統計情報を表示
        print(f"\n=== SFTデータ統計 ===")
        print(f"総データ数: {len(all_data)}")
        
        # 各タスクタイプのデータ数をカウント
        task_counts = {}
        for item in all_data:
            instruction = item['instruction']
            if 'word' in instruction.lower() and 'judge' in instruction.lower():
                if 'metaphorical' in instruction.lower():
                    if 'metaphorically used word' in instruction.lower():
                        task = 'word_judge_mword'
                    else:
                        task = 'word_judge_msent'
                else:
                    task = 'word_judge_implicit'
            elif 'sentence' in instruction.lower() and 'judge' in instruction.lower():
                if 'metaphorical' in instruction.lower():
                    if 'metaphorically used word' in instruction.lower():
                        task = 'sent_judge_mword'
                    else:
                        task = 'sent_judge_msent'
                else:
                    task = 'sent_judge_implicit'
            else:
                task = 'generation'
            
            task_counts[task] = task_counts.get(task, 0) + 1
        
        for task, count in task_counts.items():
            print(f"{task}: {count}件")

def main():
    """メイン関数"""
    print("MUNCHデータセットからSFT用データを生成します...")
    
    # データジェネレーターを初期化
    generator = MUNCHSFTDataGenerator()
    
    # 全てのSFTデータを生成
    generator.generate_all_sft_data()
    
    print("\nSFTデータの生成が完了しました！")

if __name__ == "__main__":
    main()
