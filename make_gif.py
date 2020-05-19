import imageio
import os


def create_gif(image_list, gif_name, duration = 1.0):
    '''
    :param image_list: 这个列表用于存放生成动图的图片
    :param gif_name: 字符串，所生成gif文件名，带.gif后缀
    :param duration: 图像间隔时间
    :return:
    '''
    frames = []
    print('Collecting images...')
    for image_name in image_list:
        frames.append(imageio.imread(image_name))

    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)


if __name__ == '__main__':
    path = ['./prediction/plot/',
            './prediction/describe/']

    for i, each_path in enumerate(path):
        
        image_list = []
        print('Building...')
        
        dirs = os.listdir(each_path)
        for img in dirs:
            if img[-4:] == '.png':
                image_list.append(each_path+img)

        image_list.sort()
        
        gif_name = each_path.split('/')[-2:]
        gif_name = gif_name[0] + '.gif'

        if i == 1:
            duration = 0.5
        else:
            duration = 0.1

        create_gif(image_list, gif_name, duration)
        print(f'GIF {i} completed.')
