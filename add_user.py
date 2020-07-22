from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from traceback import format_exc
import time
import os


class AddUser:
    """Class adds LinkedIn member in your chat. Require Selenium WebDriver"""
    driver = None

    def __init__(self, name_and_surname: str, chat_id: str, person_id: str):
        self.name_and_surname = name_and_surname
        self.chat_id = chat_id
        self.person_id = person_id

    @classmethod
    def login(cls, email: str, password: str):
        try:
            cls.driver.get("https://www.linkedin.com/login")
            WebDriverWait(cls.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
            WebDriverWait(cls.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
            WebDriverWait(cls.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn__primary--large"))).click()
            time.sleep(1)
            return True
        except BaseException:
            print(format_exc())
            return False

    @classmethod
    def set_driver_settings(cls):
        caps = DesiredCapabilities().FIREFOX
        caps['pageLoadStrategy'] = 'none'
        AddUser.driver = webdriver.Firefox(desired_capabilities=caps)

    def __not_the_only_one(self):
        """Return tuple of status and avatar id. This starts up if you have more than one search results."""
        AddUser.driver.execute_script("window.open();")
        AddUser.driver.switch_to.window(AddUser.driver.window_handles[1])
        AddUser.driver.get(f"https://www.linkedin.com/in/{self.person_id}/")
        status = WebDriverWait(AddUser.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2.mt1.t-18.t-black.t-normal.break-words")))
        avatar = WebDriverWait(AddUser.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                         "img.pv-top-card__photo.presence-entity__image.EntityPhoto-circle-9.lazy-image.ember-view")))
        status_text = status.text
        avatar_id = avatar.get_property("src")[39:58]
        AddUser.driver.close()
        AddUser.driver.switch_to.window(AddUser.driver.window_handles[0])
        return status_text, avatar_id

    def add(self):
        """Adds user. If the user is successfully added, returns True, otherwise returns False."""
        AddUser.driver.get(f"https://www.linkedin.com/messaging/thread/{self.chat_id}/")
        time.sleep(5)
        chat_menu = WebDriverWait(AddUser.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                            "button.msg-thread-actions__control.artdeco-button.artdeco-button--1.artdeco-button--circle.artdeco-button--tertiary.artdeco-button--muted.artdeco-dropdown__trigger.artdeco-dropdown__trigger--placement-bottom.ember-view")))
        chat_menu.click()
        chat_menu_buttons = WebDriverWait(AddUser.driver, 10).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".msg-thread-actions__dropdown-options .artdeco-dropdown__content-inner ul div")))
        chat_menu_buttons[4].click()
        search_field = WebDriverWait(AddUser.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                               ".msg-connections-typeahead__search-field.msg-connections-typeahead__search-field--no-recipients.ml1.mv1")))
        search_field.send_keys(self.name_and_surname)
        try:
            all_dt = WebDriverWait(AddUser.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "dt.t-14.t-black.t-bold.truncate")))
        except TimeoutException:
            print(AddUser.driver.find_element_by_class_name("artdeco-inline-feedback__message").text)
            return False
        if len(all_dt) > 1:
            status_and_avatar = self.__not_the_only_one()
            finded_users_avatars = WebDriverWait(AddUser.driver, 10).until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR,
                    "div.presence-entity.msg-connections-typeahead__presence-entity.presence-entity--size-2.ember-view img")))
            finded_users_statuses = WebDriverWait(AddUser.driver, 10).until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR,
                    "dl.display-flex dd.t-12.t-black--light.t-normal.truncate")))
            for i in range(len(finded_users_avatars)):
                avatar_i = finded_users_avatars[i].get_property("src")
                status_i = finded_users_statuses[i].text
                if (avatar_i[39:58] == status_and_avatar[1]) and \
                        status_i == status_and_avatar[0]:
                    finded_users_avatars[i].click()
                    break
        else:
            all_dt[0].click()
        add_user_button = WebDriverWait(AddUser.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                 "button.msg-convo-details-modal__add.ml2.flex-shrink-zero.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view")))
        add_user_button.click()
        return True



if __name__ == "__main__":
    AddUser.set_driver_settings()
    if AddUser.login(os.environ.get('EMAIL'), os.environ.get('PASSWORD')):
        milan = AddUser("Ми", "6672069181262856192", "милана-сергиенко-9365991a2")
        shabun = AddUser("Андрей Шабунько", "6672069181262856192", "андрей-шабунько-120062182")
        try:
            milan.add()
            shabun.add()
        except TimeoutException:
            print(format_exc())
        except BaseException:
            print(format_exc())
