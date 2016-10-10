## Pipeline Workflow
This repo contains pipeline configuration for a [Hello World python app](https://github.com/ttrahan/helloapp-python) for the following workflow:

```gherkin
Feature: CI/CD workflow

  Background:
    Given infrastructure on AWS
      And GitHub for source control
      And Docker Hub for docker images
      And deploying into two environments, TEST and PROD
        And these environments use DC/OS with Marathon for scheduling containers
      And uses Slack for internal communication

  Scenario: run build/CI on sample python app
    Given helloapp code base
      And use of Shippable CI configured in shippable.yml
    When a code change is committed
    Then execute a CI run
      And build docker image
      And on success, push image to registry
      And notify Slack channel of build result

  Scenario: generate deployment manifest for TEST
    Given a new image was pushed to registry
    Then update the deployment manifest for TEST environment

  Scenario: deploy to TEST environment
    Given a new manifest is created
    Then automatically trigger deployment based on the manifest to the TEST environment
      And notify Slack channel of deployment result

  Scenario: verify app in TEST and approve for promotion
    Given a successful deployment to TEST
    When deemed ready for promotion
    Then an Ops user will approve the manifest for deployment to PROD

  Scenario: deploy to PROD environment
    Given a manifest was approved for promotion to PROD
    When an Ops user manually triggers deployment to PROD
    Then update the manifest for PROD deployment
      And deploy to PROD environment
      And notify Slack channel of deployment result

  Scenario: roll back to previous deployment
    Given a second deployment to PROD environment
    When an Ops user manually triggers roll back to the prior version
    Then deploy the prior version to PROD environment
      And notify Slack channel of deployment result

```


## How to set up this demonstration

To set up this demonstration, perform the following steps:

1. Add this source code to your git-based repository (e.g. GitHub, Bitbucket, etc.)

2. Create an account on [Shippable](http://www.shippable.com)

3. Enable your repo [as a project on Shippable](http://docs.shippable.com/gs_ci_sample/#enable-a-project)

4. Create Account Integrations to store your authentication credentials for third
party services
  * [Docker Registries](http://docs.shippable.com/int_docker_registries)

5. [Assign the integrations](http://docs.shippable.com/ci_subscriptions/#integrations)
 for use by your project for the following:
  * Your GitHub, Bitbucket, etc. integration (e.g. ttrahan-gh)
  * Your Docker Hub, Amazon ECR, etc., integration (e.g. ttrahan-ecr)
  * Your Slack integration (e.g. slack)

6. Update the following in shippable.resources.yml
  * Change all integration names to match the integrations you created in 5) above
  * Change all resource locations to match your locations, e.g. change the image
  resource of type 'image' to point to your image registry repo instead of
  '288971733297.dkr.ecr.us-east-1.amazonaws.com/helloapp'

7. Add elements to your pipeline with your configuration
  * Navigate to your subscription (select from hamburger dropdown menu in upper left)
  * Select the 'SPOG' tab
  * Select the 'Resources' tab and click 'Add Resource'
  * Select your source control integration from the list
  * Select the repo and branch that hold your shippable.{jobs, resources, triggers}.yml files
  * NOTE: upon saving, you should see your pipeline configuration now appear on the SPOG tab

8. Create an Account Integration to link your CI runs to the image resource in
your pipeline
  * Go to Account Integrations (gear icon in upper right)
  * Select Integrations and click Add Integration
  * Select Event Trigger from the dropdown
  * Name your integration (e.g. ttrahan-trigger-pipeline-helloapp)
  * Assign the integration to your subscription like in 5) above (e.g. trigger-
    pipeline-helloapp)

9. Add a webhook notification to the shippable.yml file within your app repository
```yml
integrations:
  notifications:
    - integrationName: trigger-pipeline-helloapp
      type: webhook
      payload:
        - versionName=$BRANCH.$SHIPPABLE_BUILD_NUMBER
      branches:
        only:
          - github
      on_success: always
      on_failure: never
      on_start: never
```

10. Now commit a change to the app repository
  * Your pipeline should activate and you should be able to see it execute and
  deploy to TEST environment.

11. Right-click on PROD deploy job in SPOG tab of Pipelines UI and click 'Run' to
then deploy to the PROD environment.

###
