import socket
from io import StringIO

server_ip = '127.0.0.1'
server_port = 1234

buffer = StringIO()  # Dùng để ghép các mảnh dữ liệu

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((server_ip, server_port))
    print("Connected to UART over TCP.")

    while True:
        data = s.recv(1024)
        if data:
            decoded_data = data.decode('utf-8')  # Giải mã chuỗi
            buffer.write(decoded_data)          # Lưu vào buffer

            # Xử lý khi nhận được thông điệp kết thúc bằng '\n'
            if '\n' in decoded_data:
                messages = buffer.getvalue().split('\n')  # Tách chuỗi theo '\n'
                for msg in messages[:-1]:  # In các chuỗi đầy đủ
                    print(f"Received UART data: {msg}")
                buffer = StringIO()  # Tạo buffer mới chứa phần dư (nếu có)
                buffer.write(messages[-1])
        else:
            print("Connection closed by server.")
            break
except Exception as e:
    print(f"Error: {e}")
finally:
    s.close()
