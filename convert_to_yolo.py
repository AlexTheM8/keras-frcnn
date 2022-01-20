lines = []
with open('train.txt') as f:
    for line in f:
        img, x1, y1, x2, y2, label = line.split(',')
        img_name = img.split('/')[1].split('.')[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        center_x = str(((x1 + x2) / 2) / 1300)
        center_y = str(((y1 + y2) / 2) / 1000)
        width = str((x2 - x1) / 1300)
        height = str((y2 - y1) / 1000)
        with open(f'../datasets/coco128/labels/SMB/{img_name}.txt', 'w') as fn:
            fn.write(' '.join(['0', center_x, center_y, width, height]))

