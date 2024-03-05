from tkinter import *
import cv2
import os
from pyzbar.pyzbar import decode


def open_stream_IP():
    RTSP = 'rtsp://admin:admin@192.168.0.135:1935/'
    os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

    cap = cv2.VideoCapture(RTSP, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print('Поток RTSP не найден')
        exit(-1)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoded_objects = decode(frame)
        for obj in decoded_objects:
            barcode_text.insert(END, obj.data)
            barcode_text.insert(END, "\n")
            cv2.putText(frame, str(obj.data), (obj.rect.left, obj.rect.top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                        2)
            cv2.rectangle(frame, (obj.rect.left, obj.rect.top),
                          (obj.rect.left + obj.rect.width, obj.rect.top + obj.rect.height), (0, 255, 0), 2)

        cv2.imshow('Обнаружение штрихкодов', frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# Инициализация и настройка окна программы
root = Tk()
root.title("Просмотр изображения с IP-камеры")
root.geometry("480x480")

# кнопка "Открыть поток
btn1 = Button(text="Открыть RTSP поток", command=open_stream_IP)
btn1.pack(fill=X)

# поле вывода считанного штрихкода
barcode_text = Text(height=15, width=30, wrap="word")
barcode_text.pack(fill=X)

# Запуск программы
root.mainloop()