pipeline {
    agent any

    environment {
        APP_IMAGE      = "todo-app:latest"
        TEST_IMAGE     = "todo-test:latest"
        APP_CONTAINER  = "todo-app-container"
    }
    
    stages {
        stage('Code Linting') {
            steps {
                echo '=== Stage 1: Code Linting ==='
                /* Added --break-system-packages to bypass Ubuntu security restriction */
                sh '''
                    pip3 install pyflakes --quiet --break-system-packages || true
                    python3 -m pyflakes app.py || true
                    echo "Linting complete."
                '''
            }
        }

        stage('Code Build') {
            steps {
                echo '=== Stage 2: Building Docker Image ==='
                sh '''
                    docker build -t ${APP_IMAGE} .
                    echo "App image built successfully."
                '''
            }
        }

        stage('Containerized Deployment') {
            steps {
                echo '=== Stage 3: Deploying Application Container ==='
                sh '''
                    docker rm -f ${APP_CONTAINER} || true
                    docker run -d \
                        --name ${APP_CONTAINER} \
                        --network bridge \
                        -p 5000:5000 \
                        ${APP_IMAGE}
                    echo "App deployed. Waiting for startup..."
                    sleep 5
                '''
            }
        }

        stage('Containerized Selenium Testing') {
            steps {
                echo '=== Stage 4: Running Selenium Tests ==='
                sh '''
                    docker build -f Dockerfile.test -t ${TEST_IMAGE} .
                    docker run --rm \
                        --network container:${APP_CONTAINER} \
                        -e APP_URL=http://localhost:5000 \
                        ${TEST_IMAGE}
                    echo "Selenium tests completed."
                '''
            }
        }
    }

    post {
        always {
            echo '=== Cleaning up containers ==='
            /* Using double quotes allows Jenkins to inject the environment variable */
            sh "docker rm -f ${APP_CONTAINER} || true"
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs above.'
        }
    }
}