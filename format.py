import os
#遍历文件夹   
def iter_files(rootDir):
    #遍历根目录
    for root,dirs,files in os.walk(rootDir):
        for file in files:
            file_name = os.path.join(root,file)
            print(file_name)


if __name__ == "__main__":
    print(iter_files("./src"))