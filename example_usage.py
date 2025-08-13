#!/usr/bin/env python3
"""
MUNCHデータセットからSFT用データを生成する使用例

このファイルは、main.pyの使用方法を示す例です。
"""

from main import MUNCHSFTDataGenerator

def example_basic_usage():
    """基本的な使用方法の例"""
    print("=== 基本的な使用方法 ===")
    
    # データジェネレーターを初期化
    generator = MUNCHSFTDataGenerator()
    
    # 特定のタスクのSFTデータのみを生成
    print("\n1. 単語判定タスクのSFTデータを生成...")
    generator.generate_word_judgement_data(
        "tasks/word_judge.json",
        "word_judge_sft.json"
    )
    
    print("\n2. 文判定タスク（implicit）のSFTデータを生成...")
    generator.generate_sentence_judgement_data(
        "tasks/sent_judge_implicit.json",
        "sent_judge_implicit_sft.json"
    )
    
    print("\n3. 言い換え生成タスクのSFTデータを生成...")
    generator.generate_paraphrase_generation_data(
        "tasks/generation.json",
        "correct_answers/for_generation.csv",
        "generation_sft.json"
    )

def example_custom_output_directory():
    """カスタム出力ディレクトリを使用する例"""
    print("\n=== カスタム出力ディレクトリの使用例 ===")
    
    # データジェネレーターを初期化
    generator = MUNCHSFTDataGenerator()
    
    # カスタム出力ディレクトリを指定
    custom_output_dir = "my_sft_data"
    generator.generate_all_sft_data(output_dir=custom_output_dir)
    
    print(f"\nカスタムディレクトリ '{custom_output_dir}' にSFTデータが生成されました。")

def example_selective_generation():
    """選択的な生成の例"""
    print("\n=== 選択的な生成の例 ===")
    
    # データジェネレーターを初期化
    generator = MUNCHSFTDataGenerator()
    
    # 特定の条件のデータのみを生成
    print("比喩文（metaphorical sentence）の判定タスクのみを生成...")
    
    # M-sent条件の文判定タスク
    generator.generate_sentence_judgement_data(
        "tasks/sent_judge_msent.json",
        "metaphorical_sent_judge_sft.json"
    )
    
    # M-word条件の単語判定タスク
    generator.generate_word_judgement_data(
        "tasks/word_judge.json",  # word_judge.jsonには全ての条件が含まれている
        "metaphorical_word_judge_sft.json"
    )

def main():
    """メイン関数"""
    print("MUNCHデータセットからSFT用データを生成する使用例")
    print("=" * 60)
    
    # 基本的な使用方法
    example_basic_usage()
    
    # カスタム出力ディレクトリの例
    example_custom_output_directory()
    
    # 選択的な生成の例
    example_selective_generation()
    
    print("\n" + "=" * 60)
    print("使用例の実行が完了しました！")
    print("\n生成されたSFTデータは以下の形式になります：")
    print("""
{
  "instruction": "タスクの説明と入力文",
  "input": "",
  "output": "期待される回答"
}
    """)

if __name__ == "__main__":
    main()
