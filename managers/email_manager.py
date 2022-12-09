import smtplib
from typing import List, NoReturn


class EmailManager:

    def __init__(
            self,
            sender: str,
            password: str,
    ):
        self.__sender = sender
        self.__password = password

    def __login(self) -> smtplib.SMTP:
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(self.__sender, self.__password)
        return session

    def send_email(
            self,
            message: str,
            receivers: List[str],
    ) -> NoReturn:
        session = self.__login()
        for receiver in receivers:
            try:
                session.sendmail(
                    from_addr=self.__sender,
                    to_addrs=receiver,
                    msg=message,
                )
            except Exception as e:
                print(e)

        session.quit()
