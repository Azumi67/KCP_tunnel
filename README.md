به زودی اپدیت میشود.

![R (2)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/a064577c-9302-4f43-b3bf-3d4f84245a6f)
نام پروژه : تانل KCP - TCP - ICMP - IP6IP6
---------------------------------------------------------------

-----------
**توضیح کوتاه در مورد این پروژه :**

- حتما در سرور تست، نخست تانل را ازمایش کنید و سپس اقدام به استفاده از آن بکنید. این تانل را من برای مصرف شخصی و گیم استفاده میکنم .
- تمامی جوانب را در نظر بگیرید و از تانل استفاده نمایید.
- در این اسکریپت بوسیله KCP یک نوع تانل برای گیم هایم درست کردم و مدتی هست که از این تانل برای گیم هام استفاده کردم.
- برای UDP در نظر دارم که تانلی دیگر را با FEC ترکیب کنم و با زبان go که دارم مطالعه میکنم، در گیت هاب قرار بدم.
- در تانل KCP از کانفیگ خودم استفاده کردم و منابع خوبی هم نیاز دارد.
- ریست تایمر را بر اساس نیاز خودتان تعیین کنید چون مهم هست که داخل گیم دیسکانکت نشوید.
- در این تانل میتوانید از تک پورت 443 یا ازپورت رنج برای پورت تانل استفاده نمایید.من خودم همیشه از پورت رنج استفاده میکنم.
- دقت نمایید به هنگام پرسش از شما، ریست تایمر دلخواه خود را وارد نمایید تا سرویس شما بر اساس interval خاصی ریست شود.
- چرا اینکار را کردم ؟ چون سرویس گیم میباشد و مهمه است که بدانید بازه زمانی Service Reset شما چقدر است. لطفا به هنگام پاک کردن هم، همان ریست تایمر را وارد نمایید تا آن دستور پاک شود.
- خودم تمام روش ها را داخل سرور های مختلف تست کردم و جواب داده . بر روی دبیان 12 و اوبونتو 20 تست شده است.
- اگر از پنل v2ray استفاده میکنید و میخواهید با پرایوت ایپی، تانل را بسازید پس لطفا ایپی پرایوت ها را باز کنید.
- پنل شما در خارج باید نصب شده باشد
- لطفا برای کانفیگ دوباره، نخست از منوی uninstall اقدام به حذف تانل کنید تا مشکلی پیش نیاید.
- در آخر هر کانفیگ، ایپی 4 سرور ایران شما با پورت نهایی نمایش داده میشود.
- من در وقت آزاد این را درست کردم و ممکن است اشتباهاتی هم داخلش باشد. پیشاپیش ببخشید.
--------------

![Exclamation-Mark-PNG-Clipart](https://github.com/Azumi67/Game_tunnel/assets/119934376/3951d7d9-0e17-4723-b07f-786500ccbc7f)**چند نکته**

- برای تانل ICMP ، حتما اگر اشتباهی در کانفیگ انجام دادید باید حتما هم در سرور ایران و خارج حذفش کنید و هر دو سرور ریبوت شود در غیر این صورت خطای SERVER IS FULL را میگیرید.
- قبل از کانفیگ دوباره، همیشه با دستور ip a مشاهده کنید که tun0 یا tun1 که مربوط به icmp است ، موجود نباشد. حتما پس از Uninstall ICMP سرور خود را ریست نمایید.
- مورد دیگر اینکه، در سرور های ایران اگر DNS مشکل داشته باشد، ممکن است دانلود انجام نشود. حتما از طریق nano /etc/resolv.conf اقدام به تغییر موقتی dns خود بکنید .
- ممکن است در سرور ایران شما، سرعت دانلود پایین باشد و برای همین ممکن دانلود پیش نیاز ها کمی طول بکشد.
- حتما دقت نمایید برای حذف سرویس ها ، تایمر خود را به درستی وارد نمایید. به طور مثال اگر ریست تایمر شما هر 3 ساعت است ، به هنگام حذف سرویس هم، عدد 5 را وارد نمایید.
- پورت ها در آموزش برای مثال استفاده شده اند، شما میتوانید از پورت های دلخواه خودتان استفاده نمایید.


 <p align="right">
  <img src="https://github.com/Azumi67/Game_tunnel/assets/119934376/4bece965-b16a-410d-818e-dedb796f56f2" alt="Image" />
</p>

------------------------
![307981](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/39b2794b-fd04-4ae5-baea-d4b66138766e)
 **فهرست :**


 ----------------------

     

------------------------
![check](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/13de8d36-dcfe-498b-9d99-440049c0cf14)
**امکانات**
-

- پشتیبانی از TCP
- قابلیت تانل بر روی تک پورت و 5 پورت
- امکان استفاده از ایپی 6 سرور دوم خارج تنها در TCP MULTI CONFIGS
- امکان استفاده از پورت رنج برای پورت تانل
- استفاده از SMUXV2 و FEC در تانل
- کانفیگ پر سرعت برای گیم
- امکان استفاده از IP6IP6 و تانل KCP
- امکان استفاده ار ICMP و تانل KCP
- امکان حذف تمامی تانل ها و سرویس ها

**این کانفیگ برای من خیلی خوب عمل میکنه ولی برای شما ممکن است نتیجه مطلوب نباشد**

 ------------------------------------------------------

![147-1472495_no-requirements-icon-vector-graphics-clipart](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/98d8c2bd-c9d2-4ecf-8db9-246b90e1ef0f)
 **پیش نیازها**

 - لطفا سرور اپدیت شده باشه.
 - میتوانید از اسکریپت اقای [Hwashemi](https://github.com/hawshemi/Linux-Optimizer) و یا [OPIRAN](https://github.com/opiran-club/VPS-Optimizer) هم برای بهینه سازی سرور در صورت تمایل استفاده نمایید. (پیش نیاز نیست)


----------------------------

  
  ![6348248](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/398f8b07-65be-472e-9821-631f7b70f783)
**آموزش**
-
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل KCP TCP تک کانفیگ**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : KCP Tunnel TCP Single > Kharej**



 <p align="right">
  <img src="https://github.com/Azumi67/Game_tunnel/assets/119934376/e3887cfb-0eaa-4ac3-9914-b03bb0a2d349" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- حتما باید هر دو سرور ایران و خارج ایپی 6 داشته باشند. اگر سرور ایران شما ایپی 6 ندارد، از روش ICMP یا IP6IP6 و یا تانل بروکر استفاده نمایید.
- برای نصب تانل بروکر هم میتوانید از اسکریپت ایپیران  [HERE](https://github.com/opiran-club/pf-tun) استفاده نمایید.
- ایپی 6 سرور خارج را وارد نمایید
- من از پورت رنج برای پورت تانل استفاده کردم، شما میتوانید تک پورت وارد نمایید.
- پورت کانفیگ من پورت 8080 میباشد.
- برای ریستارت سرویس عدد دلخواه خود را وارد نمایید. من عدد 3 را وارد کردم پس هر 3 ساعت سرویس من ریستارت میشود. دیسکانکشن در گیم مهم است پس با دقت این عدد را وارد نمایید.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : KCP Tunnel TCP Single > IRAN**




 <p align="right">
  <img src="https://github.com/Azumi67/Game_tunnel/assets/119934376/36dae725-19bb-4a72-9da3-329eeae557ff" alt="Image" />
</p>


- سپس سرور ایران را کانفیگ میکنیم
- حتما باید هر دو سرور ایران و خارج ایپی 6 داشته باشند. اگر سرور ایران شما ایپی 6 ندارد، از روش ICMP یا IP6IP6 و یا تانل بروکر استفاده نمایید.
- ایپی 6 سرور خارج را دوباره وارد نمایید
- من از پورت رنج برای پورت تانل استفاده کردم، همان پورت هایی که وارد کردم را دوباره وارد میکنم.
- پورت کانفیگ من پورت 8080 میباشد.
- برای ریستارت سرویس عدد دلخواه خود را وارد نمایید. من عدد 3 را وارد کردم پس هر 3 ساعت سرویس من ریستارت میشود. دیسکانکشن در گیم مهم است پس با دقت این عدد را وارد نمایید.
- در سرور خارج، ریست تایمر را هر 3 ساعت گذاشتیم، پس باید در سرور ایران هم همان عدد را به کار ببریم.
- در آخر ایپی سرور شما با پورت کانفیگ شما برای استفاده در کلاینت به شما نمایش داده میشود.
- برای حذف هم مانند اسکرین زیر انجام دهید. اگر تایمر ریست را عدد 3 وارد کردید، برای حذف هم از همان عدد استفاده نمایید.

 <p align="right">
  <img src="https://github.com/Azumi67/Game_tunnel/assets/119934376/0bf9fc96-d41e-42a1-8cec-f235a7832540" alt="Image" />
</p>

--------------------------------------
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل KCP + ICMP تک کانفیگ**
-
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : KCP Tunnel ICMP Single > Kharej**



 <p align="right">
  <img src="https://github.com/Azumi67/Game_tunnel/assets/119934376/f87cdf39-9e17-423e-ba66-aa741185832b" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- اگر میخواهید توسط پرایوت ایپی 4 و تانل icmp ، تانل kcp را برقرار کنید، این روش برای شما مناسب است.
- حتما دقت نمایید که قبلا این تانل را نساخته باشید چون دیوایس جدید برای شما میسازد. پس حتما با دستور ip a از موجود نبودن آن اطمینان حاصل فرمایید.
- در صورت موجود بودن آن حتما اقدام به حذف آن نمایید و سپس سرور خود را ریبوت کنید و سپس اقدام به کانفیگ دوباره نمایید.
- من از پورت رنج برای پورت تانل استفاده کردم، شما میتوانید تک پورت وارد نمایید.
- پورت کانفیگ من پورت 8080 میباشد.
- برای ریستارت سرویس عدد دلخواه خود را وارد نمایید. من عدد 3 را وارد کردم پس هر 3 ساعت سرویس من ریستارت میشود. دیسکانکشن در گیم مهم است پس با دقت این عدد را وارد نمایید.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : KCP Tunnel ICMP Single > IRAN**



 <p align="right">
  <img src="https://github.com/Azumi67/Game_tunnel/assets/119934376/ae1dacfe-a670-42c6-a3a0-feaaa3d51dcb" alt="Image" />
</p>



- سپس سرور ایران را کانفیگ میکنیم
- مانند سرور خارج، در سرور ایران هم اطمینان حاصل فرمایید که تانل ICMP از قبل نصب نداشته باشید. ایپی 4 سرور خارج را برای برقراری تانل ICMP، وارد نمایید.
- حالا باید کانفیگ تانل KCP را انجام دهیم
- من از پورت رنج برای پورت تانل استفاده کردم، همان پورت هایی که در سرور خارج وارد کردم را دوباره وارد میکنم.
- پورت کانفیگ من پورت 8080 میباشد.
- برای ریستارت سرویس عدد دلخواه خود را وارد نمایید. من عدد 3 را وارد کردم پس هر 3 ساعت سرویس من ریستارت میشود. دیسکانکشن در گیم مهم است پس با دقت این عدد را وارد نمایید.
- در سرور خارج، ریست تایمر را هر 3 ساعت گذاشتیم، پس باید در سرور ایران هم همان عدد را به کار ببریم.
- در آخر ایپی سرور شما با پورت کانفیگ شما برای استفاده در کلاینت به شما نمایش داده میشود.
--------------------------------------
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل KCP TCP مولتی کانفیگ**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : KCP Tunnel TCP 5 CONFIGS > Kharej**



 <p align="right">
  <img src="https://github.com/Azumi67/Game_tunnel/assets/119934376/45880a58-a380-4c78-962b-e4bcb8ba4d63" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- میخواهیم از ایپی 6 استفاده نماییم پس هر دو طرف سرور باید ایپی 6 داشته باشند.
- میتوانید برای سرور ایران از تانل بروکر استفاده نمایید.
- چون منابع بالایی میخواهد بهتر از 5 کانفیگ نسازید.
- من میخواهم دو تا کانفیگ با پورت های متفاوت را در این تانل استفاده کنم. شما اگر دو تا سرور خارج دارید، ایپی 6 های هر سرور خارج را جداگانه وارد نمایید.
- به طور مثال برای کانفیگ اول پورت 8080 و ایپی 6 سرور اول ، برای کانفیگ دوم پورت دیگر و ایپی 6 سرور دوم.
- من میخواهم از ایپی 6 تک سرور استفاده کنم و دو کانفیگ با پورت 8080 و 8081 دارم.
- کانفیگ اول : ایپی 6 سرور خارج را وارد میکنم و پورت کانفیگ اول را وارد میکنم. پورت تانل کانفیگ اول هم 443 وارد میکنم
- کانفیگ دوم : ایپی 6 سرور خارج را وارد میکنم و پورت کانفیگ دوم را وارد میکنم. پورت تانل کانفیگ دوم هم 300-400 میذارم ( از پورت رنج استفاده کردم)
- میتوانید برای هر دو پورت تانل از پورت رنج استفاده نمایید.
- برای ریستارت سرویس عدد دلخواه خود را وارد نمایید. من عدد 3 را وارد کردم پس هر 3 ساعت سرویس من ریستارت میشود. دیسکانکشن در گیم مهم است پس با دقت این عدد را وارد نمایید.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : KCP Tunnel TCP 5 CONFIGS > IRAN**



 <p align="right">
  <img src="https://github.com/Azumi67/Game_tunnel/assets/119934376/dc776d6d-fd71-4a72-9068-2cad38a52ca0" alt="Image" />
</p>



- سپس سرور ایران را کانفیگ میکنیم
- میخواهیم از ایپی 6 استفاده نماییم پس هر دو طرف سرور باید ایپی 6 داشته باشند.
- میتوانید برای سرور ایران از تانل بروکر استفاده نمایید.
- چون منابع بالایی میخواهد بهتر از 5 کانفیگ نسازید.
- من میخواهم از ایپی 6 تک سرور استفاده کنم و دو کانفیگ با پورت 8080 و 8081 دارم.
- کانفیگ اول : ایپی 6 سرور خارج را وارد میکنم و پورت کانفیگ اول را وارد میکنم. پورت تانل کانفیگ اول هم 443 وارد میکنم
- کانفیگ دوم : ایپی 6 سرور خارج را وارد میکنم و پورت کانفیگ دوم را وارد میکنم. پورت تانل کانفیگ دوم هم 300-400 میذارم ( از پورت رنج استفاده کردم)
- میتوانید برای هر دو پورت تانل از پورت رنج استفاده نمایید. دقت نمایید همان پورت هایی که در سرور خارج وارد کردید بری سرور ایران هم وارد نمایید [پورت تانل]
- برای ریستارت سرویس عدد دلخواه خود را وارد نمایید. من عدد 3 را وارد کردم پس هر 3 ساعت سرویس من ریستارت میشود. دیسکانکشن در گیم مهم است پس با دقت این عدد را وارد نمایید.
- همان عددی که در سرور خارج وارد کردید هم برای سرور ایران هم انتخاب نمایید.
- در آخر ایپی سرور ایران و پورت کانفیگ شما نمایش داده میشود.
--------------------------------------
![OIP2 (1)](https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/3ec2f05f-3308-4441-8cce-62ab4776f4e2)
**تانل KCP + ICMP مولتی کانفیگ**
----------------------------------
![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : KCP Tunnel ICMP 5 CONFIGS > Kharej**



 <p align="right">
  <img src="https://github.com/Azumi67/Game_tunnel/assets/119934376/1cb8369f-5eff-4fb8-9717-953ec5f0050b" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- اگر میخواهید توسط پرایوت ایپی  4 و تانل icmp ، تانل kcp را برقرار کنید، این روش برای شما مناسب است.
- حتما دقت نمایید که قبلا این تانل را نساخته باشید چون دیوایس جدید برای شما میسازد. پس حتما با دستور ip a از موجود نبودن آن اطمینان حاصل فرمایید.
- در صورت موجود بودن آن حتما اقدام به حذف آن نمایید و سپس سرور خود را ریبوت کنید و سپس اقدام به کانفیگ دوباره نمایید.
- چون منابع بالایی میخواهد بهتر از 5 کانفیگ نسازید.
- من میخواهم دو تا کانفیگ با پورت های متفاوت را در این تانل استفاده کنم. شما اگر دو تا سرور خارج دارید، باید از گزینه TCP 5 CONFIGS استفاده نمایید.
- من میخواهم از ایپی 6 تک سرور استفاده کنم و دو کانفیگ با پورت 8080 و 8081 دارم.
- کانفیگ اول : پس از نصب ICMPTUNNEL، پورت کانفیگ اول را وارد میکنم. پورت تانل کانفیگ اول هم 443 وارد میکنم
- کانفیگ دوم : سپس پورت کانفیگ دوم را وارد میکنم. پورت تانل کانفیگ دوم هم 300-400 میذارم ( از پورت رنج استفاده کردم)
- میتوانید برای هر دو پورت تانل از پورت رنج استفاده نمایید.
- برای ریستارت سرویس عدد دلخواه خود را وارد نمایید. من عدد 3 را وارد کردم پس هر 3 ساعت سرویس من ریستارت میشود. دیسکانکشن در گیم مهم است پس با دقت این عدد را وارد نمایید.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : KCP Tunnel ICMP 5 CONFIGS > IRAN**



 <p align="right">
  <img src="https://github.com/Azumi67/Game_tunnel/assets/119934376/a9b27008-6005-4096-9eab-59211b9599d7" alt="Image" />
</p>



- سپس سرور ایران را کانفیگ میکنیم
- مانند سرور خارج، در سرور ایران هم اطمینان حاصل فرمایید که تانل ICMP از قبل نصب نداشته باشید. ایپی 4 سرور خارج را برای برقراری تانل ICMP، وارد نمایید.
- حالا باید کانفیگ تانل KCP را انجام دهیم
- چون منابع بالایی میخواهد بهتر از 5 کانفیگ نسازید.
- دو کانفیگ با پورت 8080 و 8081 دارم.
- کانفیگ اول : پورت کانفیگ اول را وارد میکنم. پورت تانل کانفیگ اول هم 443 وارد میکنم
- کانفیگ دوم : سپس پورت کانفیگ دوم را وارد میکنم. پورت تانل کانفیگ دوم هم 300-400 میذارم ( از پورت رنج استفاده کردم)
- میتوانید برای هر دو پورت تانل از پورت رنج استفاده نمایید. دقت نمایید همان پورت هایی که در سرور خارج وارد کردید بری سرور ایران هم وارد نمایید [پورت تانل]
- برای ریستارت سرویس عدد دلخواه خود را وارد نمایید. من عدد 3 را وارد کردم پس هر 3 ساعت سرویس من ریستارت میشود. دیسکانکشن در گیم مهم است پس با دقت این عدد را وارد نمایید.
- همان عددی که در سرور خارج وارد کردید هم برای سرور ایران هم انتخاب نمایید.
- در آخر ایپی سرور ایران و پورت کانفیگ شما نمایش داده میشود.
--------------------------------------

