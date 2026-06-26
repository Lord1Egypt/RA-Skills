import os
import pandas as pd


def del_file(path):
    try:
        if if_exist(path) is True:
            os.remove(path)
            return True
        return False
    except OSError:
        print("Error: delete file {0} is failed!".format(path))
        return False


def if_exist(path):
    return os.path.exists(path)


def save_csv(df, file_name, overwrite=True):
    # 使用UTF-8-SIG编码（带BOM的UTF-8），兼容Excel和所有Unicode字符
    encoding = 'utf-8-sig'
    
    if overwrite is True:
        del_file(file_name)
        df.to_csv(file_name, encoding=encoding, header=True, index=False)
    else:
        if not os.path.isfile(file_name):
            df.to_csv(file_name, encoding=encoding, header=True, index=False)
        else:
            # 追加模式时也需要指定编码
            with open(file_name, 'a', encoding=encoding) as f:
                df.to_csv(f, header=False, mode='a', index=False)
    return


# 读取csv文件
def read_csv(path, header=0, index_col=None, encoding=None):
    if if_exist(path) is False:
        return None
    
    # 尝试自动检测编码
    if encoding is None:
        encodings_to_try = ['utf-8-sig', 'gbk', 'gb2312', 'gb18030', 'latin1', 'cp936', 'utf-8']
        for enc in encodings_to_try:
            try:
                df = pd.read_csv(path, header=header, index_col=index_col, encoding=enc)
                return df
            except:
                continue
        # 如果所有编码都失败，使用默认编码
        encoding = 'utf-8-sig'
    
    df = pd.read_csv(path, header=header, index_col=index_col, encoding=encoding)
    if df is None or df.shape[0] < 1:
        return None
    return df


def read_excel(path, header=0, index_col=None, encoding="GBK"):
    if if_exist(path) is False:
        return None
    df = pd.read_excel(path,header=header,index_col=index_col)
    # df = pd.read_csv(path, header=header, index_col=index_col, encoding=encoding)
    if df is None or df.shape[0] < 1:
        return None
    return df


def make_dirs(path):
    if os.path.exists(path) is False:
        os.makedirs(path, exist_ok=True)


# 创建文件
def make_file(path):
    dirs = os.path.split(path)[0]
    if os.path.exists(dirs) is False:
        os.makedirs(dirs)
    f = open(path, 'w')
    f.close()


def get_current_path():
    return os.path.abspath('.')  # 获得当前工作目录
