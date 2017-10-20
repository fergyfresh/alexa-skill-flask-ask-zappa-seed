Alexa Skill with Flask-Ask Zappa seed project
=============================================


Introduction
------------

This project creates a microservice deployed on AWS API Gateway and Lambda and provides the API Gateway HTTPS Url
in Alexa Developer portal.

Architecture
------------

.. image:: /images/alexa-skill.png
    :alt: Alexa Skill Service Design

Tools and Technologies
-----------------------

*  Python 2.7
*  `Flask-Ask`_: Flask-Ask is a Flask extension that makes building Alexa skills for the Amazon Echo.
*  `cookiecutter-flask-ask`_: ready-to-roll Alexa Skill skeleton based on Flask-Ask
*  `Zappa`_: Serverless framework for Lambda and API Gateway using python
*  `Tox`_: virtualenv management and test command line tool using pytest
*  `Sphinx`_: Documentation generator
*  AWSCli: AWS command line tool

.. _Flask-Ask: https://github.com/johnwheeler/flask-ask
.. _cookiecutter-flask-ask: https://github.com/chrisvoncsefalvay/cookiecutter-flask-ask
.. _Zappa: https://www.zappa.io/
.. _Tox: https://tox.readthedocs.io/en/latest/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/

Security
--------

For better AWS security use custom AWS VPC and Security Group, add below configuration in your ``zappa_settings.json`` file

.. code-block:: json

    "vpc_config": {
        "SubnetIds": [ "subnet-12345678" ],
        "SecurityGroupIds": [ "sg-12345678" ]
    }

Setup
-----

It is recommended to run this project in a virtualenv. If virtualenvs are unfamiliar to you, `this handy tutorial`_
might be a good place to start.

**Create Virtual Environment**

#.  Install virtualenv: ``$ pip install virtualenv``
#.  Create virtual environment names env: ``$ virtualenv env``
#.  Activate env on Unix: ``$ source venv/bin/activate``
#.  Activate env on Windows: ``$ env\Scripts\activate``
#.  Install the required Python packages from root project folder: ``$ pip install -r requirements.txt --no-cache-dir``

.. _this handy tutorial: http://docs.python-guide.org/en/latest/dev/virtualenvs/

**AWS Deployment**

*Create AWS User*

#.  Create an IAM user named ``Zappa-Deploy`` in the AWS console
#.  Give ``AdministratorAccess`` policy for this user
#.  Once the user is created, its Access key ID and Secret access key are displayed, keep it safe

*Configure IAM credentials locally*

#.  Make sure you are in project root folder and virtual env is active
#.  Configure AWS: ``$ aws configure``
#.  Follow the prompts to input your ``Access key ID`` and ``Secret access key``.
#.  For Default region name, type: ``us-east-1``.
#.  For Default output format: ``json``.

This will install credentials and configuration in an ``.aws`` directory inside your home directory

*Deploy the skill with Zappa*

#.  ``zappa_settings.json`` file has all required configuration to deploy dev to AWS
#.  Very first time execute: ``$ zappa deploy dev``
#.  Releasing code updates doesn't recreate the API gateways and is a faster. Such updates are handled through a separate command: ``$ zappa update dev``
#.  API Gateway url will be displayed on cosole something like: ``https://abcdefgh.execute-api.us-east-1.amazonaws.com/dev``

**Configure the skill in the Alexa developer console and test**

#.  Working with the Alexa console requires `Alexa Developer console`_ access
#.  Go to `Alexa Skills list`_ page
#.  Click the Add a New Skill button
#.  The skill configuration screen opens

.. _Alexa Developer console: https://developer.amazon.com
.. _Alexa Skills list: https://developer.amazon.com/edw/home.html#/skills

*Skill Information section*

#.  Set the Name of the skill and Invocation Name

*Interaction Model section*

#.  Paste in the ``Intent Schema``
#.  Create ``Custom Slot type``
#.  Paste in the ``Sample Utterances``

*Configuration section*

#.  Select HTTPS as the Service Endpoint Type
#.  Paste API Gateway url

*SSL Certificate section*

#.  Select the option that reads: ``My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority``

*Test Section*

Now test the skill by typing: What is news

Also, you can check `This video`_ by `John Wheeler`_ which shows how to deploy your speech assets configuration to the `Alexa Developer Portal`_.

That's all! If you are using a browser that supports WebRTC for micophone input (Chrome, Firefox or Opera),
you may use `echosim`_ to test your script - simply log in with the same credentials you used to deploy your Skill.

.. _Alexa Developer Portal: https://developer.amazon.com/alexa
.. _This video: https://alexatutorial.com
.. _John Wheeler: https://alexatutorial.com/flask-ask/
.. _echosim: http://www.echosim.io/

Testing and Code Coverage
-------------------------

To run tests and check code coverage, execute below command in root project directory

``$ tox``

This will create python 2.7 virtual environment and execute the tests

To clean run the tests execute ``$ tox --recreate``

Zappa Commands
--------------

*  Logs - ``$ zappa tail dev``
*  Limit the output returned and eliminate the HTTP noise in the logs by using the --since 1m and --non-httpcommand options: ``$ zappa tail dev --since 1m --non-http``
*  Remove the AWS Lambda function, API gateway: ``$ zappa undeploy dev``

Sphinx Commands
---------------

#.  Go to <root_folder>/docs and execute below commands to create HTML documents
#.  Unix: ``$ make html``
#.  Windows: ``make.bat html``

Useful Links
------------

*   Tutorial - `Flask-ask skill with zappa`_
*   `Flask-ask blog`_
*   `Defining utterances`_ for alexa skill kit
*   Alexa skill kit `training videos`_
*   `Alexa Skills w/ Python and Flask-Ask`_
*   `Introducing echosim.io`_
*   `Alexa Skill Demo`_

.. _Flask-ask skill with zappa: https://developer.amazon.com/blogs/post/8e8ad73a-99e9-4c0f-a7b3-60f92287b0bf/new-alexa-tutorial-deploy-flask-ask-skills-to-aws-lambda-with-zappa
.. _Flask-ask blog: https://developer.amazon.com/blogs/post/Tx14R0IYYGH3SKT/Flask-Ask-A-New-Python-Framework-for-Rapid-Alexa-Skills-Kit-Development
.. _Defining utterances: http://www.makermusings.com/2015/07/21/defining-utterances-for-the-alexa-skills-kit/
.. _training videos: https://developer.amazon.com/alexa-skills-kit/alexa-skills-developer-training#templates
.. _Alexa Skills w/ Python and Flask-Ask: https://pythonprogramming.net/intro-alexa-skill-flask-ask-python-tutorial/
.. _Introducing echosim.io: https://developer.amazon.com/blogs/alexa/post/Tx3BB1JHNS1TDTS/introducing-echosim-io-a-new-online-tool-built-by-the-community-for-the-community
.. _Alexa Skill Demo: https://github.com/ModusCreateOrg/alexa-skill-demo



