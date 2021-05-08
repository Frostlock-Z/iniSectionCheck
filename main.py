import re
import subprocess
import tkinter.filedialog
import time
# import os
from pathlib import Path


def main():
    # 创建字典，里面保存每个file中存在的section
    files = {}
    # 创建list，里面保存所有文件中出现过的section
    common_sections = []
    # 调用tkinter的选择文件
    filenames = tkinter.filedialog.askopenfilenames(title='选择一个ini文件', filetypes=[('配置设置', '*.ini'), ('所有文件', '*')],
                                                    initialdir=Path.cwd())
    # 如果未选择文件则直接退出程序
    if len(filenames) == 0:
        return
    # 生成输出文件，顺便试下str format
    f_time = Path.cwd().joinpath(
        "iniSectionCheck{0}.txt".format(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))))
    output_file = open(f_time, mode="w")

    # 判断被选择的文件是否还存在，不一定用有用，还没找到例外
    for filename in filenames:
        if not is_ini_exist(filename):
            print(filename, "文件不存在，程序终止。")
            output_file.write("%s 文件不存在，程序终止。\n" % filename)
            return
        else:
            print(filename, "文件存在。")
            output_file.write("%s 文件存在。\n" % filename)

    # 文件对比开始
    print()
    print("===================单文件对比开始===================")
    output_file.write("\n===================单文件对比开始===================\n")
    # 遍历所有保存的文件名，选择文件
    for filename in filenames:
        # 创建字典保存文件中section
        sections = {}
        # 打开文件
        file = open(filename)

        print("文件：", filename)
        output_file.write("文件：%s \n" % filename)

        # re库可以用来进行正则表达式判断
        # 以下是获取[]以及其中内容的正则
        pattern = re.compile(r'(?m)^\[[^]\r\n]+]')
        # 遍历ini中的内容
        for line in file:
            # 试图获取匹配项
            result = pattern.match(line)
            # 判断如果获取不为None
            if result:
                # 获取匹配字符串
                section = result.group()
                # 判断字符串是否在字典中
                if section in sections:
                    # 如果存在，则给计数+1
                    sections[section] += 1
                else:
                    # 如果不存在，则记录到字典并设置值为1
                    sections[section] = 1
                # 记录下出现过的section，并记录到list中
                if section not in common_sections:
                    common_sections.append(section)

        # 记录下当前文件中是否有重复项
        single_file_count = 0
        for k in sections:
            if sections[k] > 1:
                print("存在重复项：", k, "出现次数：", sections[k])
                output_file.write("存在重复项：%s 出现次数：%d。\n" % (k, sections[k]))
                single_file_count += 1

        if single_file_count == 0:
            print("在文件中未发现重复项。")
            output_file.write("在文件中未发现重复项。\n")

        files[filename] = sections
        file.close()

    print("===================单文件对比结束===================")
    output_file.write("===================单文件对比开始===================\n")

    print()
    print("===================多文件对比开始===================")
    output_file.write("\n===================多文件对比开始===================\n")
    multi_files_count = 0
    for section in common_sections:
        files_list = []
        for f in files:
            if section in files[f]:
                files_list.append(f)
        if len(files_list) > 1:
            multi_files_count += 1
            print("项：", section, "同时存在于以下文件：")
            output_file.write("项：%s 同时存在于以下文件：\n" % section)
            for c in files_list:
                print(c)
                output_file.write("%s\n" % c)
        print()
        output_file.write("\n")
    if multi_files_count == 0:
        print("在多文件中未发现重复项。")
        output_file.write("在多文件中未发现重复项。\n")
    print("===================多文件对比结束===================")
    output_file.write("===================多文件对比结束===================\n")
    output_file.close()
    # os.system(str(f_time))
    subprocess.run(["notepad", str(f_time)])


def is_ini_exist(path: str) -> bool:
    exist = Path(path).exists()
    return exist


if __name__ == "__main__":
    main()
