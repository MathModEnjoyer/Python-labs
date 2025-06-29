import analyzerdf
import time
import threading
import logging
from meteostat import Daily, Point

class CancellationToken:
    '''
    Класс токена отмены выполнения задачи.
    '''
    def __init__(self):
        self.__is_canceled = False

    def is_canceled(self) -> bool:
        '''
        Метод проверки отмены задачи.
        Returns:
            True, если задача была отменена.
        '''
        return self.__is_canceled

    def cancel(self) -> None:
        '''
        Метод установки статуса отмены выполнения задачи.
        '''
        self.__is_canceled = True

class Service:
    '''
    Класс сервиса анализатора.
    '''
    def __init__(self,
                 analyzer: analyzerdf.Analyzer):
        '''
        Конструктор сервиса.
        Args:
            analyzer: обработчик задачи.
        '''
        self.__cancellation_token = None
        self.__logger = logging.getLogger(__name__)
        self.__analyzer = analyzer
        self.__thread = None

    def start(self,
              file_path: str = 'file.txt'):
        '''
        Метод запуска сервиса.
        Args:
            file_path - путь до файла записи.
        '''
        if self.__thread is not None:
            error = RuntimeError("Попытка повторного запуска сервиса")
            self.__logger.warning(error)
            raise error
        self.__cancellation_token = CancellationToken()
        self.__thread = threading.Thread(target=self.__run,
                                         args=(file_path,
                                               self.__cancellation_token))
        try:
            self.__thread.start()
            self.__logger.info("Сервис запустился")
        except:
            error = RuntimeError("Не удалось запустить сервис")
            self.__logger.error(error)
            raise error

    def stop(self):
        '''
        Метод остановки сервиса.
        '''
        if self.__thread is None:
            error = RuntimeError("Попытка остановить незапущенный сервис")
            self.__logger.warning(error)
            raise error
        self.__cancellation_token.cancel()
        self.__thread.join()
        self.__thread = None
        self.__logger.info("Сервис завершил работу")

    def __run(self,
              file_path: str = 'file.txt',
              cancellation_token: CancellationToken = CancellationToken()):

        while (not cancellation_token.is_canceled()):
            self.__analyzer._data_frame = Daily(
                            Point(self.__analyzer.point[0],
                            self.__analyzer.point[1], 
                            self.__analyzer.point[2]), 
                            self.__analyzer._data_frame.index[-1],
                            self.__analyzer._data_frame.index[-1] + 
                            (self.__analyzer._data_frame.index[-1] - 
                            self.__analyzer._data_frame.index[0])).fetch()
            
            try:
                with open(file_path, 'a') as f:
                    f.write(str(self.__analyzer.get_differential()) + '\n')
            except:
                error = RuntimeError("Не удалось записать данные в файл," +
                                     "сервис завершает работу")
                self.__logger.error(error)
            time.sleep(7)
