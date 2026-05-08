pipeline {
    agent any

    environment {
        APP_IMAGE      = "todo-app:latest"
        TEST_IMAGE     = "todo-test:latest"
        APP_CONTAINER  = "todo-app-container"
        NETWORK_NAME   = "todo-net"
    }

    stages {
        stage('Code Linting') {
            steps {
                echo '=== Stage 1: Code Linting ==='
                sh '''
                    pip3 install pyflakes --quiet --break-system-packages || true
                    python3 -m pyflakes app.py || true
                '''
            }
        }

        stage('Code Build') {
            steps {
                echo '=== Stage 2: Building Docker Image ==='
                sh "docker build -t ${APP_IMAGE} ."
            }
        }

        stage('Containerized Deployment') {
            steps {
                echo '=== Stage 3: Deploying on Shared Network ==='
                sh '''
                    # Network create karo agar nahi bana
                    docker network create ${NETWORK_NAME} || true
                    
                    # Purana container hatao
                    docker rm -f ${APP_CONTAINER} || true
                    
                    # App ko todo-net network par chalao
                    docker run -d \
                        --name ${APP_CONTAINER} \
                        --network ${NETWORK_NAME} \
                        -p 5000:5000 \
                        ${APP_IMAGE}
                    
                    echo "Waiting for app to start..."
                    sleep 10
                '''
            }
        }

        stage('Containerized Selenium Testing') {
            steps {
                echo '=== Stage 4: Running Selenium Tests ==='
                sh '''
                    # Test image build karo
                    docker build -f Dockerfile.test -t ${TEST_IMAGE} .
                    
                    # Test container ko bhi todo-net par chalao
                    # Yahan localhost ki jagah container name use hoga
                    docker run --rm \
                        --network ${NETWORK_NAME} \
                        -e APP_URL=http://${APP_CONTAINER}:5000 \
                        ${TEST_IMAGE}
                '''
            }
        }
    }

    post {
        always {
            echo '=== Cleanup ==='
            sh "docker rm -f ${APP_CONTAINER} || true"
        }
        success {
            echo '✅ SUCCESS: Pipeline passed!'
        }
        failure {
            echo '❌ FAILED: Check logs.'
        }
    }
}