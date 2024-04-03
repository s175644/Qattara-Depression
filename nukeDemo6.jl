using GLPK, Cbc, JuMP, SparseArrays, LinearAlgebra, NPZ, NLsolve

H = npzread("Height data.npy")

S1 = [
300 140 40
]

S2 = [
500 230 60
]

S3 = [
1000 400 70
]

function constructA(H,K)
    k0=fill((K[1]),size(H))
    k1=fill(K[2],size(H)[1]-1)
    k2=fill(K[3],size(H)[1]-2)
    a=diagm(0 => k0, 1 => k1, 2 => k2)
    A=Symmetric(a)
    return A
end

set = [S1, S2, S3]

function solveIP(H, set)
    CHD = 10
    h = ceil(Int, length(H)/1.5)
    myModel = Model(Cbc.Optimizer)
    # If your want ot use GLPK instead use:
    #myModel = Model(GLPK.Optimizer)
    A = constructA(H,set[1])
    B = constructA(H,set[2])
    C = constructA(H,set[3])
    D = cat(A,B,dims=3)
    E = cat(D,C,dims=3)

    @variable(myModel, x[1:h, 1:3], Bin )
    @variable(myModel, R[1:h] >= 0 )
    @variable(myModel, Diffabs[1:h])

    @objective(myModel, Min, sum(Diffabs[j] for j=1:h) )

    @constraint(myModel, [j=1:h],R[j] >= H[j] + CHD )
    @constraint(myModel, [i=1:h],R[i] == sum(E[i,j,k]*x[j,k] for j=1:h, k=1:3) )
    @constraint(myModel, [j=1:h],(R[j]-H[j]-CHD) <= Diffabs[j])
    @constraint(myModel, [j=1:h],-(R[j]-H[j]-CHD) <= Diffabs[j])
    @constraint(myModel, [j=1:h-1], sum(x[j,:])+sum(x[j+1,:]) <= 1)
    @constraint(myModel, [j=1:h], sum(x[j,:]) <= 1)

    optimize!(myModel)

    if termination_status(myModel) == MOI.OPTIMAL
        println("Objective value: ", JuMP.objective_value(myModel))
        println("x = ", JuMP.value.(x))
        println("R = ", JuMP.value.(R))
        npzwrite("Locations6.npy", JuMP.value.(x))
        npzwrite("ChannelDepth6.npy", JuMP.value.(R))
    else
        println("Optimize was not succesful. Return code: ", termination_status(myModel))
    end
end

solveIP(H, set)