На локальных серверах не определяет ip адрес, поэтому использовал
    client_ip = '77.47.236.2'
По необходимости изменить на
    client_ip = request.META.get('REMOTE_ADDR')