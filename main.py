#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка
from PIL import Image
from PIL.ImageQt import ImageQt # для перевода графики из Pillow в Qt 
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
   )

app = QApplication([])
mw = QWidget()
mw.resize(700, 700)
mw.setWindowTitle('Easy editer')

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_blac_white = QPushButton('Ч/Б')
btn_save = QPushButton('Сохранить')
btn_reset = QPushButton('Сбросить фильтры')
btn_folder = QPushButton('Папка')
btn_blur = QPushButton('Блюр')
btn_emboss = QPushButton('Emboss')
btn_find_edges = QPushButton('Find_Edges')
btn_smooth = QPushButton('Smooth')

lw_files = QListWidget()
lb_image = QLabel('картинка')

row = QHBoxLayout()
row_2 = QHBoxLayout()
col_1 = QVBoxLayout()
col_2 = QVBoxLayout()

col_1.addWidget(btn_folder)
col_1.addWidget(lw_files)

row_2.addWidget(btn_left)
row_2.addWidget(btn_right)
row_2.addWidget(btn_mirror)
row_2.addWidget(btn_sharp)
row_2.addWidget(btn_blac_white)
row_2.addWidget(btn_save)
row_2.addWidget(btn_reset)
row_2.addWidget(btn_blur)
row_2.addWidget(btn_emboss)
row_2.addWidget(btn_find_edges)
row_2.addWidget(btn_smooth)

col_2.addWidget(lb_image)
col_2.addLayout(row_2)
row.addLayout(col_1)
row.addLayout(col_2)

Workdir = ''
def chooseWorkdir():
   global Workdir
   Workdir = QFileDialog.getExistingDirectory()

def Filter(files, extensions):
   result = []
   for filename in files:
      for extension in extensions:
         if filename.endswith(extension):
            result.append(filename)
   return result      

def showFilenamesList():
   extensions = ['.jpg', '.jpeg', 'png', '.bmp']
   chooseWorkdir()
   filenames = Filter(os.listdir(Workdir), extensions)  
   lw_files.clear()
   for filename in filenames:
      lw_files.addItem(filename)

class ImageProcessor():
   def __init__(self):
      self.image = None
      self.filename = None
      self.save_dir = 'Modified/'
      self.original_image = None

   def LoadImage(self, filename):
      self.filename = filename
      image_path = os.path.join(Workdir, filename)
      self.image = Image.open(image_path)
      self.original_image = self.image.copy()

   def ShowImage(self, image):
      qimage = ImageQt(image)
      pixmapeimage = QPixmap.fromImage(qimage)
      width, height = lb_image.width(), lb_image.height()
      scaled_paxmap = pixmapeimage.scaled(width, height, Qt.KeepAspectRatio)
      lb_image.setPixmap(scaled_paxmap)
      lb_image.setVisible(True)

   def SaveImage(self):
      try:
         path = os.path.join(Workdir, self.save_dir)
         if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
         image_path = os.path.join(path, self.filename)
         self.image.save(image_path)
      except:
         pass


   def do_bw(self):
      self.image = self.image.convert('L')
      self.ShowImage(self.image)

   
   def mirror(self):
      try:
         self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
         self.ShowImage(self.image)
      except:
         pass
   
   def do_left(self):
      try:
         self.image = self.image.transpose(Image.ROTATE_90) 
         self.ShowImage(self.image)
      except:
         pass

   def do_right(self):
     try:
        self.image = self.image.transpose(Image.ROTATE_270) 
        self.ShowImage(self.image)
     except:
        pass

   def reset(self):
      try:
         self.image = self.original_image.copy()
         self.ShowImage(self.image)
      except:
         pass
  
   def do_sharp(self):
      try:
         self.image = self.image.filter(SHARPEN)
         self.ShowImage(self.image)
      except:
         pass

   def do_emboss(self):
      try:
         self.image = self.image.filter(EMBOSS)
         self.ShowImage(self.image)
      except:
         pass

   def do_blur(self):
      try:
         self.image = self.image.filter(GaussianBlur)
         self.ShowImage(self.image)
      except:
         pass

   def find_edges(self):
      try:
         self.image = self.image.filter(FIND_EDGES)
         self.ShowImage(self.image)
      except:
         pass

   def do_smooth(self):
      try:
         self.image = self.image.filter(SMOOTH_MORE)
         self.ShowImage(self.image)
      except:
         pass

   def do_wb(self):
      try:
         if self.image.mode == 'L':
            self.reset()
         elif self.image.mode == 'RGB':
            self.do_bw()
      except:
         pass
            

workimage = ImageProcessor()   

def ShowChosenImage():
   if lw_files.currentRow() >= 0:
      filename = lw_files.currentItem().text()
      workimage.LoadImage(filename)
      image_path = os.path.join(Workdir, workimage.filename)
      workimage.ShowImage(image_path)

lw_files.currentRowChanged.connect(ShowChosenImage)

btn_blac_white.clicked.connect(workimage.do_wb)
btn_mirror.clicked.connect(workimage.mirror)
btn_save.clicked.connect(workimage.SaveImage)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_reset.clicked.connect(workimage.reset)
btn_sharp.clicked.connect(workimage.do_sharp)
btn_blur.clicked.connect(workimage.do_blur)
btn_emboss.clicked.connect(workimage.do_emboss)
btn_find_edges.clicked.connect(workimage.find_edges)
btn_smooth.clicked.connect(workimage.do_smooth)


btn_folder.clicked.connect(showFilenamesList)
mw.setLayout(row)
mw.show()
app.exec()
