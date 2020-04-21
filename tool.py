import os


class Tool:
    """colab操作中的工具，包含克隆仓库到colab，下载kaggle数据集"""

    def __init__(self, compete_name='', gdrive_path='/content/gdrive/', colab_config_path='My Drive/colab_config/'):
        """初始化类
        Parameters
        ---------
        compete_name: str
            kaggle compete 名称
        dgrive_path: str
            google drive 挂载的路径
        colab_config_path: str
            配置文件存放路径，目前包含kaggle配置文件、github personal access token存放文件
        """
        self.compete_name = compete_name
        self.gdrive_path = gdrive_path
        self.colab_config_path = gdrive_path + colab_config_path
        print(os.popen('pip install kaggle --upgrade').read())
        os.putenv('KAGGLE_CONFIG_DIR', self.colab_config_path)

    def write_kaggle_config(self, content):
        """写入kaggle配置文件
        Parameters
        ----------
        content: str
            kaggle 配置文件内容， 格式为{"username":"xxx","key":"xxxxxxx"}
        """
        with open(self.colab_config_path + 'kaggle.json', 'w') as f:
            try:
                f.write(content)
            except (Exception, IOError) as identifier:
                print(identifier)
                return

            print('写入成功')

    def write_github_token(self, content):
        """写入github personal access token
        Parameters
        ----------
        content: str
            github personal access token
        """
        with open(self.colab_config_path + 'github_token.txt', 'w') as f:
            f.write(content)
            print('完成token写入')

    def get_github_token(self):
        """获取存放的github personal access token"""
        with open(self.colab_config_path + 'github_token.txt', 'w') as f:
            token = token = f.read().replace('\n', '')
            self.token = token
            return self.token

    def clone_github(self, rep='WeMiracle/publicTool.git'):
        """克隆github仓库
        Parameters
        ---------
        rep: str
            仓库位置，连同用户名
        """
        self.get_github_token()
        print(
            os.popen(f'git clone https://{self.token}@github.com/{rep}').read())

    def download(self, compete_name='', dst='./'):
        '''下载kaggle平台数据集
        Parameters
        -----
        compete_name: str
            数据集名称, 默认为初始化此类时传入的compete_name参数
        dst: str
            数据集下载存放路径， 默认为当前目录
        '''
        if not compete_name:
            compete_name = self.compete_name
        
        print("######### has installed kaggle ######")
        print(
            os.popen(f'kaggle competitions download -p {dst} {compete_name} ').read())

    def submission(self, file_path, message='上传文件', compete_name=''):
        """上传预测结果到kaggle平台

        Parameters
        ----------
        file_path: str
            需上传的文件路径和名称
        message: str
            备注信息
        compete_name: str
            kaggle compete 名称，默认为初始化时传入的compete_name
        """
        if not compete_name:
            compete_name = self.compete_name
        os.putenv('KAGGLE_CONFIG_DIR', self.colab_config_path)
        print("######### has installed kaggle ######")
        # kaggle competitions submit -c digit-recognizer -f submission.csv -m "Message"
        print(os.popen(
            f'kaggle competitions submit -c {compete_name} -f {file_path} -m "{message}" ').read())

    def draw_acc(self, history, plt):
        """绘制训练过程中损失/准确度曲线

        Parameters
        ----------
        history: tf.keras.callbacks.History
            model fit返回的history对象
        plt: matplotlib.pyplt
            matplotlib.pyplt
        """
        acc = history.history['acc']
        val_acc = history.history['val_acc']
        loss = history.history['loss']
        val_loss = history.history['val_loss']

        epochs = range(len(acc))
        plt.plot(epochs,     acc)
        plt.plot(epochs, val_acc)
        plt.title('Training and validation accuracy')
        plt.figure()
        plt.plot(epochs,     loss)
        plt.plot(epochs, val_loss)
        plt.title('Training and validation loss')
        plt.legend()
        plt.show()
