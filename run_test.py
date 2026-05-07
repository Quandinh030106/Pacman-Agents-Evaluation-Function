import subprocess
import time
import csv
import os

MSSV = 24521425

algorithms = ['MinimaxAgent', 'AlphaBetaAgent', 'ExpectimaxAgent']
eval_functions = ['scoreEvaluationFunction', 'betterEvaluationFunction']


maps = ['testClassic', 'minimaxClassic', 'trappedClassic', 'smallClassic', 'mediumClassic']
seeds = [MSSV + i for i in range(5)]

output_filename = "KetQua_ThucNghiem_Pacman.csv"

print(f"Bắt đầu chạy thực nghiệm")
print(f"Tổng cộng: {len(algorithms)} x {len(eval_functions)} x {len(maps)} x {len(seeds)} = {len(algorithms)*len(eval_functions)*len(maps)*len(seeds)} ván game.")

with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Thuật Toán', 'Hàm Lượng Giá', 'Map', 'Seed', 'Kết Quả', 'Điểm Số', 'Thời Gian (giây)'])

    total_runs = 0
    for eval_fn in eval_functions:
        for algo in algorithms:
            for map_name in maps:
                for seed in seeds:
                    total_runs += 1
                    
                    cmd = [
                        'python', 'pacman.py', 
                        '-l', map_name, 
                        '-p', algo, 
                        '-a', f'depth=3,evalFn={eval_fn}', 
                        '-s', str(seed), 
                        '-q'
                    ]

                    print(f"[{total_runs}/150] Đang chạy: {algo} | {eval_fn} | {map_name} | Seed {seed}...")
                    
                    start_time = time.time()
                    process = subprocess.run(cmd, capture_output=True, text=True)
                    end_time = time.time()
                    duration = round(end_time - start_time, 4)

                    output = process.stdout
                
                    if "Pacman emerges victorious!" in output:
                        result = "Win"
                    elif "Pacman died!" in output:
                        result = "Lose"
                    else:
                        result = "Error/Timeout"
                    score = 0
                    for line in output.split('\n'):
                        if "Score:" in line:
                            try:
                                score = int(line.split(":")[-1].strip())
                            except:
                                pass

                    writer.writerow([algo, eval_fn, map_name, seed, result, score, duration])

                    file.flush()
                    os.fsync(file.fileno())

print(f"\nĐã lưu toàn bộ kết quả vào file: {output_filename}")